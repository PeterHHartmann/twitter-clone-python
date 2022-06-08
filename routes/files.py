from bottle import get, response, static_file
from io import BytesIO
import traceback
import db.database as db
from datetime import datetime

@get('/style/<stylesheet_name>')
def _(stylesheet_name):
    return static_file(stylesheet_name, root='public/style', mimetype='text/css')

@get('/js/<script_name>')
def _(script_name):
    return static_file(script_name, root='public/javascript', mimetype='application/x-javascript')

@get('/image/<image_name>')
def _(image_name):
    return static_file(image_name, root='public/image', mimetype='image/*')

@get('/image/profile_picture/<user_name>/<image_name>')
def _(user_name, image_name):
    try:
        user = db.user_select_by_username(user_name)
        profile_picture = db.avatar_select(user['user_id'])
        if profile_picture['image_blob']:
            stream = BytesIO(profile_picture['image_blob'])
            bytes = stream.read()

            last_modified_str = profile_picture['last_modified'].strftime('%a, %d %b %Y %H:%M:%S GMT')
            response.set_header('Content-Type', 'image/*')
            response.set_header('Last-Modified', last_modified_str)
            response.set_header("Cache-Control", "public, max-age=604800")
            return bytes
        else:
            response.status = 404
            return
    except:
        traceback.print_exc()
        response.status = 404
        return

@get('/image/banner/<user_name>/<image_name>')
def _(user_name, image_name):
    try:
        user = db.user_select_by_username(user_name)
        banner = db.banner_select(user['user_id'])
        if banner['image_blob']:
            stream = BytesIO(banner['image_blob'])
            bytes = stream.read()

            last_modified_str = banner['last_modified'].strftime('%a, %d %b %Y %H:%M:%S GMT')
            response.set_header('Content-Type', 'image/*')
            response.set_header('Last-Modified', last_modified_str)
            response.set_header("Cache-Control", "public, max-age=604800")
            return bytes
        else:
            response.status = 404
            return
    except:
        traceback.print_exc()
        response.status = 404
        return

@get('/tweet/<tweet_id>/<image_name>')
def _(tweet_id, image_name):
    try:
        tweet_image = db.tweet_image_select(image_name)
        if tweet_image:
            stream = BytesIO(tweet_image['image_blob'])
            bytes = stream.read()
            response.set_header('Content-Type', 'image/*')
            response.set_header("Cache-Control", "public, max-age=604800")
            return bytes
        else:
            response.status = 404
            return
    except:
        traceback.print_exc()
        response.status = 404
        return
