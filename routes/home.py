from bottle import get, view, redirect, request
from utility.validation import get_jwt

@get('/')
@view('index')
def _():
    payload = get_jwt()
    if not payload:
        return redirect('/login')

    if request.query.get('signedin'):
        return dict(toast_msg='You have successfully logged in', **payload)
    return payload