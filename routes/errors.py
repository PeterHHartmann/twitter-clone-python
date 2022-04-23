from bottle import error, view

@error(404)
@view('404')
def _(error):
    return