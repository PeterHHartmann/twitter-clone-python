from datetime import datetime
from bottle import get, view, abort, redirect, post, response, request
from utility.validation import get_jwt
import db.database as db
import traceback
import os
import imghdr

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

def upload_image(type, image, user_name):
    file_name, file_extension = os.path.splitext(image.filename)
    if file_extension not in ('.png', '.jpeg', '.jpg'):
        raise Exception('image not allowed')
    image_name = f"{user_name}{file_extension}"
    full_path = f"public/image/user/{type}/{image_name}"
    print(dir(image))
    try:
        image.save(full_path)
    except:
        os.remove(full_path)
        image.save(full_path)
    # imghdr_extension = imghdr.what(f"public/image/users/{image_name}")
    # if file_extension != f".{imghdr_extension}":
    #     print('mmm... suspicious ... it is not really an image')
    #     os.remove(f'public/image/user/{image_name}')
    #     return 'mmm... got you! It was not an image'
    return


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
            try:
                upload_image('pfp', pfp, user_name)
            except:
                traceback.print_exc()
                response.status = 500
                return
        if banner:
            try:
                upload_image('banner', banner, user_name)
            except:
                traceback.print_exc()
                response.status = 500
                return
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

