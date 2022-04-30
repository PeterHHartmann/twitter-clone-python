from bottle import get, view, abort
from utility.validation import get_session, login_required
import db.database as db

@get('/admin')
@view('admin')
@login_required
def _():
    session = get_session()
    if session['user_name'] == 'admin':
        all_tweets = db.tweets_get_all()
        return dict(**session, all_tweets=all_tweets)
    abort(404)
