from bottle import get, post, request, response, redirect, view
import json
import traceback
import bcrypt
import re
from random import randint
import time
from uuid import uuid4

import db.database as db
from utility.validation import set_jwt, get_jwt, send_validation_email
from utility.regex_str import REGEX_EMAIL, REGEX_USER_NAME, REGEX_PASSWORD

@get('/login')
@view('login')
def _():
    session = get_jwt()
    if session:
        if session.get('status'):
            return redirect(f'/auth/{session["status"]["url_snippet"]}')
        return redirect('/')
    else: 
        return

@post('/login')
def _():
    data = json.load(request.body)
    input = {
        'email': data.get('email'),
        'pwd': data.get('pwd'),
    }
    if not input['email'] or len(input['email'].strip()) < 1:
        response.status = 400
        return dict(msg='Please enter an email')
    if not re.match(REGEX_EMAIL, input['email']):
        response.status = 400
        return dict(msg='Please enter a valid email')
    if not input['pwd'] or len(input['pwd'].strip()) < 1:
        response.status = 400
        return dict(msg='Please enter a password')

    try:
        user = db.user_get_by_email(input['email'])

        # check if input pwd doesn't match db password
        if bcrypt.checkpw(bytes(input['pwd'], 'utf-8'), bytes(user['user_pwd'], 'utf-8')):
            details = db.details_get(user_name=user['user_name'])
            payload = {
                'user_name': user['user_name'],
                'user_email': user['user_email'],
                'display_name': details['display_name']
            }
            try:
                # check if user has validated their email 
                # if they haven't return redirect url with error code 403: Forbidden
                validation = db.validation_get_by_email(user['user_email'])
                if validation:
                    payload['status'] = {'verified': False, 'url_snippet': validation['validation_url']}
                    set_jwt(payload)
                    response.status = 403
                    return dict(url_snippet=validation['validation_url'])
            finally:
                set_jwt(payload)
                return
        # otherwise proceed with login process
        else:
            response.status = 401
            return dict(msg='Invalid email or password')
    except:
        traceback.print_exc()
        response.status = 401
        return dict(msg='Invalid email or password')

@get('/signup')
@view('signup')
def _():
    cookie = request.get_cookie("JWT", secret="secret_info")
    if cookie:
        return redirect('/')
    else:
        return

@post('/signup')
def _():
    data = json.load(request.body)

    display_name = data.get('display_name').strip()
    if len(display_name) < 1:
        response.status = 400
        return dict(msg='Please enter a display name')
    if len(display_name) > 50:
        response.status = 400
        return dict(msg='Display name is too long (Maximum 50 characters')

    #TODO no white spaces in username
    user_name = data.get('user_name').strip()
    if len(user_name) < 3:
        response.status = 400
        return dict(msg='Username must be longer than 3 characters long')
    if len(user_name) > 50:
        response.status = 400
        return dict(msg='Username is too long (Maximum 50 characters)')
    if not re.match(REGEX_USER_NAME, user_name):
        response.status = 400
        return dict(msg='Please enter a valid username')

    user_email = data.get('user_email')
    if not re.match(REGEX_EMAIL, user_email):
        response.status = 400
        return dict(msg='Please enter a valid email')
    user_pwd = data.get('user_pwd')
    if len(user_pwd) < 6 or len(user_pwd) > 20:
        response.status = 400
        return dict(msg='Password must be longer than 6 or shorter than 20 characters')
    if not re.match(REGEX_PASSWORD, user_pwd):
        response.status = 400
        return dict(msg='Please enter a valid password')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(user_pwd, 'utf_8'), salt).decode('utf-8')

    try:
        validation = {
            'code': randint(100000, 999999),
            'url_snippet': str(uuid4())
        }

        print(validation['code'])
        user = dict(
            user_name=user_name,
            user_email=user_email,
            user_pwd=hashed)

        details = dict(display_name=display_name, joined_date=time.now())

        db.user_post(user, validation, details)
        send_validation_email(validation['url_snippet'], validation['code'], user_name)
        return dict(url_snippet=validation['url_snippet'])
        
    except Exception as e:
        traceback.print_exc()
        response.status = 400
        if str(e) == 'UNIQUE constraint failed: users.user_name':
            return dict(msg='That username is taken')
        elif str(e) == 'UNIQUE constraint failed: users.user_email':
            return dict(msg='That email is already in use')

@get('/logout')
def _():
    response.delete_cookie("JWT", secret="secret_info")
    return redirect('/login')