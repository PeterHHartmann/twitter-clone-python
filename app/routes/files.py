from bottle import get, response, static_file
from io import BytesIO
import traceback
import database as db
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
        profile_picture = db.profile_picture_get(user_name)
        if profile_picture['image_blob']:
            stream = BytesIO(profile_picture['image_blob'])
            bytes = stream.read()

            last_modified_str = datetime.fromtimestamp(profile_picture['last_modified']).strftime('%a, %d %b %Y %H:%M:%S GMT')
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
        banner = db.banner_get(user_name)
        if banner['image_blob']:
            stream = BytesIO(banner['image_blob'])
            bytes = stream.read()

            last_modified_str = datetime.fromtimestamp(banner['last_modified']).strftime('%a, %d %b %Y %H:%M:%S GMT')
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
        tweet_image = db.tweet_get_image(tweet_id)
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
