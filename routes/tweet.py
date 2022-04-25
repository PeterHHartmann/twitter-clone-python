import traceback
from bottle import post, request, response, redirect, delete
import db.database as db
from utility.validation import get_jwt
import json

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
            if len(tweet['tweet_text'].strip()) <= 1:
                response.status = 403
                return 

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
            response.status = 500
            return
    else:
        response.status = 403
        return

@post('/tweet/edit/<tweet_id>')
def _(tweet_id):
    session = get_jwt()
    if session:
        data = json.load(request.body)
        print(tweet_id)
        print(data['tweet_text'])
        try:
            db.tweet_update(tweet_id, data['tweet_text'])
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    else:
        response.status = 403
        return

@delete('/tweet/delete/<tweet_id>')
def _(tweet_id):
    session = get_jwt()
    if session:
        try:
            db.tweet_delete(tweet_id)
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    else:
        response.status = 403
        return
