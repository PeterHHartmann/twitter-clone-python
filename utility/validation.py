from dotenv import load_dotenv
load_dotenv()
from functools import wraps
from bottle import request, response, redirect
import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib 
import ssl
import json
import traceback

def set_session(payload):
    encoded_jwt = jwt.encode(payload=payload, key="secret_jwt", algorithm="HS256")
    cookie_opts = {
        # keep session for 3 days
        'max_age': 3600 * 24 * 3,

        # for security
        'httponly': True,
        'secure': request.headers.get('X-Forwarded-Proto') == 'https',
    }
    try:
        import production
        cookie_value = encoded_jwt.decode('utf-8')
    except:
        traceback.print_exc()
        cookie_value = encoded_jwt
    response.set_cookie(name="JWT", value=json.dumps(cookie_value), secret="secret_info", **cookie_opts)

def get_session():
    try:
        cookie = request.get_cookie("JWT", secret="secret_info")
        parsed = json.loads(cookie)
        data = jwt.decode(parsed, key="secret_jwt", algorithms=["HS256"])
        return data
    except:
        return None

def send_validation_email(url, code, user_name, user_email):
    sender_email = os.getenv('EMAIL')

    try:
        import production
        receiver_email = user_email
    except:
        receiver_email = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PW')

    message = MIMEMultipart("alternative")
    message["Subject"] = "Not Twitter Email Confirmation"
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        import production
        full_url = f'https://peterhartmann.eu.pythonanywhere.com/auth/{url}'
    except:
        full_url = f'http://localhost:3000/auth/{url}'

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi, {user_name}
    Thank you for signing up to Not Twitter.
    Please visit: {full_url} to confirm your email
    Your verification code is: {code}
    """

    html = f"""\
    <html>
        <body>
        <h2 style="color: rgb(29, 155, 240)">Hi, {user_name}.</h2>
        <h3>Thank you for signing up to Not Twitter.</h3>
        <span>
            <p>Your verification code is: </p>
            <h1 style="color: rgb(51, 51, 51)">{code}</h1>
        </span>
        <p>Please visit <a href="{full_url}">this link</a> to confirm your email</p>
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        except:
            traceback.print_exc()
    return

def api_login_required(func):
    """Make sure user is logged in before proceeding. 
    Otherwise return status 403: Forbidden"""
    @wraps(func)
    def wrapper_login_required(*args, **kwargs):
        session = get_session()
        if session is None:
            response.status = 403
            return
        return func(*args, **kwargs)
    return wrapper_login_required

def login_required(func):
    """Make sure user is logged in before proceeding.
    Otherwise redirect to login"""
    @wraps(func)
    def wrapper_login_required(*args, **kwargs):
        session = get_session()
        if session is None:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper_login_required