import traceback
from bottle import post, request, response, redirect
import db.database as db
from utility.validation import get_jwt
import time
import traceback

@post('/tweet/<user_name>')
def _(user_name):
    session = get_jwt()
    if session:
        try:
            now = time.time()
            tweet = {
                'tweet_text': request.forms.get('tweet_text'),
                'tweet_timestamp': now
            }
            tweet_img = request.files.get('tweet_img')
            # print(tweet_img)
            if tweet_img:
                tweet['tweet_img'] = tweet_img.file.read()
            else: 
                tweet['tweet_img'] = None

            tweet_id = db.tweet_post(user_name, tweet)
            print(tweet_id)
            time_ms = round(now * 1000, 0)
            return dict(tweet_id=tweet_id, tweet_timestamp = time_ms)

        except:
            traceback.print_exc()
            response.status = 401
            return
    else:
        return redirect('/login')