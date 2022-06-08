from bottle import get, view
from utility.validation import login_required, get_session
import db.database as db
from datetime import datetime

@get('/')
@view('index')
@login_required
def home():
    session = get_session()
    tweets_from_follows = db.tweets_select_by_following(session['user_id'])
    test = tweets_from_follows[0]['created_at']
    epoch = datetime.utcfromtimestamp(0)
    print( (test - epoch).total_seconds() * 1000 )
    # print(test.strftime('%S'))
    who_to_follow = db.profiles_select_who_to_follow(session['user_id'])
    profile_picture = db.avatar_select(session['user_id'])
    return dict(**session, tweets_from_follows=tweets_from_follows, who_to_follow=who_to_follow, profile_picture=profile_picture)