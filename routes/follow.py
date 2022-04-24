from bottle import get, post, redirect, response
from utility.validation import get_jwt
import traceback
import db.database as db

@get('/follow/whotofollow')
def _():
    payload = get_jwt()
    if not payload:
        return redirect('/login')
    try:
        users = db.user_get_many(payload['user_name'])
        return dict(users=users)
    except:
        traceback.print_exc()
        response.status = 500
        return

@post('/follow/<user_to_follow>')
def _(user_to_follow):
    session = get_jwt()
    if session:
        try:
            db.follow_post(session['user_name'], user_to_follow)
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    else:
        return redirect('/login')