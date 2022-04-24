from bottle import get, response, static_file
from io import BytesIO
import traceback
import db.database as db

@get('/style/<stylesheet_name>')
def _(stylesheet_name):
    return static_file(stylesheet_name, root='public/style', mimetype='text/css')

@get('/js/<script_name>')
def _(script_name):
    return static_file(script_name, root='public/javascript', mimetype='application/x-javascript')

@get('/image/<image_name>')
def _(image_name):
    return static_file(image_name, root='public/image', mimetype='image/*')

@get('/image/<user_name>/<identifier>.jpg')
def _(user_name, identifier):
    try:
        user_images = db.details_get_images(user_name)
        if user_images:
            stream = BytesIO(user_images[str(identifier)])
            bytes = stream.read()
            response.set_header('Content-Type', 'image/*')
            return bytes
        else:
            response.status = 404
            return
    except:
        response.status = 404
        return

@get('/tweet/<tweet_id>/twimg.jpg')
def _(tweet_id):
    try:
        content = db.tweet_get_image(tweet_id)
        if content:
            stream = BytesIO(content['tweet_img'])
            bytes = stream.read()
            response.set_header('Content-Type', 'image/*')
            return bytes
            return
        else:
            response.status = 404
            return
    except:
        traceback.print_exc()
        response.status = 404
        return
