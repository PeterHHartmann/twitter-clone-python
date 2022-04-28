from bottle import get, view, redirect, request
from utility.validation import get_jwt
import db.database as db

@get('/')
@view('index')
def _():
    session = get_jwt()
    if not session:
        return redirect('/login')

    tweets_from_follows = db.tweets_get_following(session['user_name'])
    who_to_follow = db.details_get_many(session['user_name'])
    profile_picture = db.profile_picture_get(session['user_name'])

    return dict(**session, tweets_from_follows=tweets_from_follows, who_to_follow=who_to_follow, profile_picture=profile_picture['image_name'])