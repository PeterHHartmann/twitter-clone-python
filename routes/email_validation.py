from bottle import get, post, view, redirect, request, response
import traceback
import json
from random import randint

from utility.validation import set_session, get_session, send_validation_email
import db.database as db

@get('/auth/<url_code>')
@view('email-validation')
def _(url_code):
    try:
        validation = db.verification_select_by_url_snippet(url_code)
        return dict(user_name=validation['user_name'], user_email=validation['email'], confirmation_url=url_code)
    except:
        traceback.print_exc()
        return redirect('/login')

@post('/auth/<url_code>/resend')
def _(url_code):
    data = json.load(request.body)
    try:
        new_code = randint(100000, 999999)
        user = db.user_select_by_email(data['user_email'])
        db.verification_update_code(user['user_id'], new_code)
        send_validation_email(url_code, new_code, data['user_name'], data['user_email'])
        return
    except:
        traceback.print_exc()
        response.status = 500
        return dict(msg='something went wrong sorry')

@post('/auth/<url_code>')
def _(url_code):
    data = json.load(request.body)
    try:
        confirmation = db.verification_select_by_url_snippet(url_code)
        if confirmation:
            if confirmation['verification_code'] == int(data['code']):
                user = db.user_select_by_email(data['user_email'])
                db.verification_delete(user['user_id'])
                return
            else:
                response.status = 403
                return dict(msg='Wrong code please try again')
        else:
            response.status = 403
            return dict(msg='Wrong code please try again')
    except:
        traceback.print_exc()
        response.status = 500
        return dict(msg='Something went wrong, please try again later')