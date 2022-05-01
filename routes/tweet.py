from bottle import post, request, response, put, delete
import db.database as db
from utility.validation import get_session, api_login_required
import json
import uuid
import imghdr
import time
import traceback

@post('/tweet')
@api_login_required
def _():
    print('it got through')
    session = get_session()
    try:
        now = time.time()
        tweet = {
            'tweet_text': request.forms.get('tweet_text'),
            'tweet_timestamp': now
        }
        tweet_img = request.files.get('tweet_img')
        image_name = None
        if tweet_img:
            image = tweet_img.file
            image_extension = f'.{imghdr.what(image)}'
            if image_extension not in ('.png', '.jpeg', '.jpg', '.gif'):
                response.status = 403
                return
            image_name = str(uuid.uuid4())
            full_image_name = f"{image_name}{image_extension}"
            tweet['image_name'] = full_image_name
            tweet['image_blob'] = tweet_img.file.read()

        tweet_id = db.tweet_post(session['user_name'], tweet)
        time_ms = round(now * 1000, 0)
        return dict(tweet_id=tweet_id, tweet_timestamp = time_ms, image_name=image_name)
    except:
        traceback.print_exc()
        response.status = 500
        return

@put('/tweet/<tweet_id>')
@api_login_required
def _(tweet_id):
    session = get_session()
    tweet = db.tweet_get(tweet_id)
    if tweet.get('user_name') == session['user_name']:
        try:
            data = json.load(request.body)
            db.tweet_update(tweet_id, data['tweet_text'])
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    response.status = 403
    return

@delete('/tweet/<tweet_id>')
@api_login_required
def _(tweet_id):
    session = get_session()
    try:
        tweet = db.tweet_get(tweet_id)
        if tweet.get('user_name') == session['user_name']:
            db.tweet_delete(tweet_id)
            return
        else:
            response.status = 403
            return
    except:
        traceback.print_exc()
        response.status = 500
        return
