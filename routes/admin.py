from bottle import get, view, redirect, request, abort
from utility.validation import get_jwt
import db.database as db

@get('/admin')
@view('admin')
def _():
    session = get_jwt()
    if not session:
        return redirect('/login')

    if session['user_name'] == 'admin':
        all_tweets = db.tweets_get_all()
        return dict(**session, all_tweets=all_tweets)
    else:
        abort(404)
