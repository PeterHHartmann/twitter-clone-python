from datetime import datetime
from bottle import get, view, abort, redirect, post, response, request
from utility.validation import get_jwt
import db.database as db
import traceback
import imghdr
import time
import uuid

@get('/user/<user_name>')
@view('user')
def _(user_name):
    payload = get_jwt()
    if not payload:
        return redirect('/login')
    try:
        user = db.user_get_by_username(user_name)
        details = db.details_get(user_name)
        joined_month = datetime.fromtimestamp(details['joined_date']).strftime('%B')
        joined_year = datetime.fromtimestamp(details['joined_date']).strftime('%Y')
        user_tweets = db.tweets_get_by_user(user_name)

        profile = dict(
            user_name       =   user['user_name'], 
            display_name    =   details['display_name'], 
            bio             =   details['bio'],
            joined_month    =   joined_month, 
            joined_year     =   joined_year,
            picture         =   details['pfp_image_name'],
            banner          =   details['banner_image_name']
        )

        who_to_follow = db.details_get_many(payload['user_name'])

        session_profile_picture = db.profile_picture_get(payload['user_name'])

        return dict(**payload, profile=profile, who_to_follow=who_to_follow, user_tweets=user_tweets, profile_picture=session_profile_picture['image_name'])
    except:
        traceback.print_exc()
        abort(404)

@post('/user/edit/<user_name>')
def _(user_name):
    payload = get_jwt()
    if not payload:
        return redirect('/login')
    if payload['user_name'] == user_name:
        pfp = request.files.get('pfp')
        banner = request.files.get('banner')
        details = {
            'display_name': request.forms.get('display_name'),
            'bio': request.forms.get('bio')
        }
        if pfp:
            image = pfp.file
            image_extension = f'.{imghdr.what(image)}'
            if image_extension not in ('.png', '.jpeg', '.jpg', '.gif'):
                response.status = 403
                return
            image_name = uuid.uuid4()
            full_image_name = f"{image_name}{image_extension}"
            db.profile_picture_update(payload['user_name'], dict(image_name=full_image_name, image_blob=image.read(), last_modified=time.time()))

        if banner:
            image = banner.file
            image_extension = f'.{imghdr.what(image)}'
            if image_extension not in ('.png', '.jpeg', '.jpg', '.gif'):
                response.status = 403
                return
            image_name = uuid.uuid4()
            full_image_name = f"{image_name}{image_extension}"
            db.banner_update(payload['user_name'], dict(image_name=full_image_name, image_blob=image.read(), last_modified=time.time()))
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

