from bottle import get, response, abort, static_file
from io import BytesIO
import traceback
import db.database as db

@get('/style/<stylesheet_name>')
def _(stylesheet_name):
    return static_file(stylesheet_name, root='public/style')

@get('/js/<script_name>')
def _(script_name):
    return static_file(script_name, root='public/javascript')

@get('/image/<image_name>')
def _(image_name):
    return static_file(image_name, root='public/image')

@get('/image/<user_name>/<identifier>.jpg')
def _(user_name, identifier):
    try:
        user_images = db.details_get_images(user_name)
        stream = BytesIO(user_images[str(identifier)])
        bytes = stream.read()
        response.set_header('Content-Type', 'image/jpeg')
        return bytes
    except:
        traceback.print_exc()
        abort(404)