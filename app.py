from bottle import run, TEMPLATE_PATH, default_app, request

TEMPLATE_PATH.insert(0, 'public/views')

### routing
import routes.files
import routes.home
import routes.auth
import routes.email_validation
import routes.user
import routes.follow
import routes.tweet
import routes.errors

try:
    import production
    application = default_app()
except:
    run(host='127.0.0.1', port=3000, debug=True, reloader=True)
