from bottle import get, view
from utility.validation import login_required, get_session
import database as db

@get('/')
@view('index')
@login_required
def home():
    session = get_session()
    tweets_from_follows = db.tweets_get_following(session['user_name'])
    who_to_follow = db.details_get_who_to_follow(session['user_name'])
    profile_picture = db.profile_picture_get(session['user_name'])
    return dict(**session, tweets_from_follows=tweets_from_follows, who_to_follow=who_to_follow, profile_picture=profile_picture['image_name'])