from datetime import datetime
from bottle import get, view, abort, redirect, post, response, request
from utility.validation import get_jwt
import db.database as db
import traceback

@get('/user/<user_name>')
@view('user')
def view_user(user_name):
    payload = get_jwt()
    if not payload:
        return redirect('/login')
    try:
        user = db.user_get_by_username(user_name)
        details = db.details_get(user_name)
        joined_month = datetime.fromtimestamp(details['joined_date']).strftime('%B')
        joined_year = datetime.fromtimestamp(details['joined_date']).strftime('%Y')

        user_tweets = db.tweets_get_by_user(user_name)

        body = dict(
            profile_user_name       =   user['user_name'], 
            profile_display_name    =   details['display_name'], 
            profile_bio             =   details['bio'],
            profile_joined_month    =   joined_month, 
            profile_joined_year     =   joined_year,
            **payload,
            user_tweets = user_tweets

        )
        return body
    except:
        traceback.print_exc()
        abort(404)

@post('/user/edit/<user_name>')
def _(user_name):
    payload = get_jwt()
    if not payload:
        return redirect('/login')
    if payload['user_name'] == user_name:
        current_imgs = db.details_get_images(user_name)
        pfp = request.files.get('pfp')
        banner = request.files.get('banner')
        details = {
            'display_name': request.forms.get('display_name'),
            'bio': request.forms.get('bio')
        }
        if pfp:
            details['pfp'] = pfp.file.read()
        else:
            details['pfp'] = current_imgs['pfp']
        if banner:
            details['banner'] = banner.file.read()
        else:
            details['banner'] = current_imgs['banner']
        try:
            db.details_update(user_name, details)
            return
        except:
            traceback.print_exc()
            response.status = 500
            return
    else:
        response.status = 403
        return

