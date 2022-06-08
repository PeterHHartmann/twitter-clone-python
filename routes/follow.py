from bottle import post, delete, response
from utility.validation import get_session, api_login_required
import traceback
import db.database as db

@post('/follow/<user_to_follow>')
@api_login_required
def _(user_to_follow):
    session = get_session()
    try:
        db.follow_insert(session['user_id'], user_to_follow)
        return
    except:
        traceback.print_exc()
        response.status = 500
    return

@delete('/follow/<user_to_follow>')
@api_login_required
def _(user_to_follow):
    session = get_session()
    if session.get('user_id'):
        try:
            db.follow_delete(session['user_id'], user_to_follow)
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    response.status = 403
    return