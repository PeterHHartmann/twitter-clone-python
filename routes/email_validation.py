from bottle import get, post, view, redirect, request, response
import traceback
import json
from random import randint

from utility.validation import set_jwt, get_jwt, send_validation_email
import db.database as db

@get('/auth/<url_code>')
@view('email-validation')
def _(url_code):
    try:
        validation = db.validation_get_by_url(url_code)
        return dict(user_name=validation['user_name'], user_email=validation['user_email'], confirmation_url=url_code)
    except:
        traceback.print_exc()
        return redirect('/signup')

@post('/auth/<url_code>/resend')
def _(url_code):
    data = json.load(request.body)
    try:
        new_code = randint(100000, 999999)
        db.validation_update_code(data['user_email'], new_code)
        send_validation_email(url_code, new_code, data['user_name'])
        return
    except:
        traceback.print_exc()
        response.status = 500
        return dict(msg='something went wrong sorry')

@post('/auth/<url_code>')
def _(url_code):
    data = json.load(request.body)
    try:
        confirmation = db.validation_get_by_url(url_code)
        if confirmation:
            if confirmation['validation_code'] == int(data['code']):
                db.validation_delete(dict(user_email=data['user_email']))

                # try to remove the email validation field on JWT on cookie
                try:
                    payload = get_jwt()
                    del payload['status']
                    set_jwt(payload)
                finally:
                    return
            else:
                response.status = 401
                return dict(msg='Wrong code please try again')
        else:
            response.status = 401
            return dict(msg='Wrong code please try again')
    except:
        traceback.print_exc()
        response.status = 500
        return dict(msg='Something went wrong, please try again later')