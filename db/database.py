import sqlite3
import json

DB_PATH = 'db/database.sqlite'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def user_get_by_email(user_email):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        user = db.execute('SELECT * FROM users WHERE user_email=:user_email', dict(user_email=user_email)).fetchone()
        return user
    finally:
        db.close()

def user_get_by_username(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        user = db.execute('''
            SELECT * 
            FROM users 
            WHERE user_name=:user_name
        ''', dict(user_name=user_name)).fetchone()
        return user
    finally:
        db.close()

def user_post(user, validation, details):
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        cursor.execute('INSERT INTO users(user_name, user_email, user_pwd) VALUES(:user_name, :user_email, :user_pwd)', user)
        cursor.execute('INSERT INTO email_validations(user_email, validation_url, validation_code) VALUES(:user_email, :validation_url, :validation_code)', dict(user_email=user['user_email'], validation_url=validation['url_snippet'], validation_code=validation['code']))
        cursor.execute('INSERT INTO user_details(user_name, display_name, joined_date) VALUES(:user_name, :display_name, :joined_date)', dict(user_name=user['user_name'], display_name=user['user_name'], **details))
        cursor.execute('INSERT INTO profile_pictures(user_name, last_modified) VALUES(:user_name, :last_modified);', dict(user_name=user['user_name'], last_modified=details['joined_date']))
        cursor.execute('INSERT INTO banners(user_name, last_modified) VALUES(:user_name, :last_modified);', dict(user_name=user['user_name'], last_modified=details['joined_date']))
        db.commit()
    finally:
        db.close()

#TODO get users with the most followers once implemented
def details_get_who_to_follow(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        user = json.dumps(db.execute('''
            SELECT 
                user_details.user_name, 
                user_details.display_name,
                profile_pictures.image_name AS pfp_image_name, 
                banners.image_name AS banner_image_name,
                users.user_email
            FROM user_details 
            JOIN profile_pictures ON profile_pictures.user_name = user_details.user_name
            JOIN banners ON banners.user_name = user_details.user_name
            JOIN users ON users.user_name = user_details.user_name
            LEFT JOIN email_validations ON email_validations.user_email = users.user_email
            WHERE NOT user_details.user_name=:user_name
            AND NOT user_details.user_name="admin"
            AND email_validations.user_email IS NULL
            AND users.user_name IN (
                SELECT DISTINCT u.user_name
                FROM users u
                LEFT OUTER JOIN follows f
                ON f.user_name = u.user_name
                WHERE NOT u.user_name = :user_name
                AND NOT u.user_name IN (
                    SELECT ff.follows_user
                    FROM follows ff
                    LEFT OUTER JOIN users uu
                    ON ff.user_name = uu.user_name
                    WHERE uu.user_name = :user_name
                )
            )
            ORDER BY joined_date DESC 
            LIMIT 10;
        ''', dict(user_name = user_name)).fetchall())
        return json.loads(user)
    finally:
        db.close()

def details_get(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        details = json.dumps(db.execute('''
            SELECT
                user_details.user_name, 
                user_details.display_name, 
                user_details.bio, 
                user_details.joined_date, 
                profile_pictures.image_name AS pfp_image_name, 
                banners.image_name AS banner_image_name
            FROM user_details
            JOIN profile_pictures ON profile_pictures.user_name = user_details.user_name
            JOIN banners ON banners.user_name = user_details.user_name
            JOIN users ON users.user_name = user_details.user_name
            LEFT JOIN email_validations ON email_validations.user_email = users.user_email
            WHERE user_details.user_name=:user_name
            AND email_validations.user_email IS NULL
            LIMIT 1;
            ''', dict(user_name=user_name)).fetchone())
        return json.loads(details)
    finally:
        db.close()

def details_update(user_name, details):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute('''
            UPDATE user_details
            SET 
            display_name=:display_name, 
            bio=:bio
            WHERE user_name=:user_name;
            ''', dict(user_name=user_name, **details))
        db.commit()
    finally:
        db.close()

def profile_picture_get(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        profile_picture = db.execute('''
            SELECT image_name, image_blob, last_modified
            FROM profile_pictures
            WHERE user_name=:user_name
            LIMIT 1
            ''', dict(user_name=user_name)).fetchone()
        return profile_picture
    finally:
        db.close()

def profile_picture_update(user_name, profile_picture):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute('''
            UPDATE profile_pictures
            SET 
            image_name=:image_name, 
            image_blob=:image_blob, 
            last_modified=:last_modified
            WHERE user_name=:user_name;
            ''', dict(user_name=user_name, **profile_picture))
        db.commit()
    finally:
        db.close()

def banner_get(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        profile_picture = db.execute('''
            SELECT image_name, image_blob, last_modified
            FROM banners
            WHERE user_name=:user_name
            ''', dict(user_name=user_name)).fetchone()
        return profile_picture
    finally:
        db.close()

def banner_update(user_name, banner):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute('''
            UPDATE banners
            SET 
            image_name=:image_name, 
            image_blob=:image_blob, 
            last_modified=:last_modified
            WHERE user_name=:user_name;
            ''', dict(user_name=user_name, **banner))
        db.commit()
    finally:
        db.close()

def tweet_post(user_name, tweet):
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
            VALUES(:user_name, :tweet_text, :tweet_timestamp)
            ''', dict(user_name=user_name, **tweet))
        tweet_id = cursor.lastrowid
        if tweet.get('image_blob'):
            cursor.execute('''
                INSERT INTO tweet_images(tweet_id, image_name, image_blob)
                VALUES(:tweet_id, :image_name, :image_blob)
            ''', dict(tweet_id=tweet_id, image_name=tweet['image_name'], image_blob=tweet['image_blob']))
        db.commit()
        return tweet_id
    finally:
        db.close()

def tweet_get_image(tweet_id):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        content = db.execute('''
            SELECT tweet_id, image_name, image_blob
            FROM tweet_images
            WHERE tweet_id=:tweet_id
            ''', dict(tweet_id=tweet_id)).fetchone()
        return content
    finally:
        db.close()

def tweet_update(tweet_id, tweet_text):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute(
            '''
            UPDATE tweets
            SET tweet_text=:tweet_text
            WHERE tweet_id=:tweet_id;
            ''', dict(tweet_text=tweet_text, tweet_id=tweet_id))
        db.commit()
    finally:
        db.close()

def tweet_delete(tweet_id):
    try:
        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        cursor.execute(
            '''
            DELETE FROM tweet_images
            WHERE tweet_id=:tweet_id;
            ''', dict(tweet_id=tweet_id))
        cursor.execute(
            '''
            DELETE FROM tweets
            WHERE tweet_id=:tweet_id;
            ''', dict(tweet_id=tweet_id))
        db.commit()
    finally:
        db.close()

def tweets_get_by_user(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        tweets = db.execute(
            '''
            SELECT 
                tweets.user_name, 
                user_details.display_name, 
                profile_pictures.image_name AS pfp_image_name,
                tweets.tweet_id, 
                tweets.tweet_text, 
                tweets.tweet_timestamp,
                tweet_images.image_name
            FROM tweets
            LEFT JOIN tweet_images ON tweets.tweet_id = tweet_images.tweet_id
            JOIN user_details ON tweets.user_name = user_details.user_name
            JOIN profile_pictures ON profile_pictures.user_name = user_details.user_name
            WHERE tweets.user_name=:user_name
            ORDER BY tweets.tweet_timestamp DESC;
            ''', dict(user_name=user_name)).fetchall()
        return tweets
    finally:
        db.close()

def tweets_get_following(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        tweets = db.execute(
            '''
            SELECT 
                user_details.user_name, 
                user_details.display_name, 
                profile_pictures.image_name AS pfp_image_name, 
                tweets.tweet_id, 
                tweets.tweet_text, 
                tweets.tweet_timestamp,
                tweet_images.image_name
            FROM tweets
            LEFT JOIN tweet_images ON tweets.tweet_id = tweet_images.tweet_id
            JOIN user_details ON tweets.user_name = user_details.user_name
            JOIN profile_pictures ON profile_pictures.user_name = user_details.user_name
            WHERE user_details.user_name IN (
                SELECT f.follows_user
                FROM follows f
                JOIN users u
                ON (f.user_name = u.user_name)
                WHERE u.user_name = :user_name
            ) OR tweets.user_name=:user_name
            ORDER BY tweets.tweet_timestamp DESC;
            ''', dict(user_name=user_name)).fetchall()
        return tweets
    finally:
        db.close()

def tweets_get_all():
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        tweets = db.execute(
            '''
            SELECT 
                user_details.user_name, 
                user_details.display_name, 
                tweets.tweet_id, 
                tweets.tweet_text, 
                tweets.tweet_timestamp,
                tweet_images.image_name
            FROM tweets
            LEFT JOIN tweet_images ON tweets.tweet_id = tweet_images.tweet_id
            JOIN user_details ON tweets.user_name = user_details.user_name
            ORDER BY tweets.tweet_timestamp DESC;
            ''').fetchall()
        return tweets
    finally:
        db.close()

def follow_post(user_name, follows_user):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute('''
            INSERT INTO follows(user_name, follows_user)
            VALUES(:user_name, :follows_user)
        ''', dict(user_name=user_name, follows_user=follows_user))
        db.commit()
    finally:
        db.close()

def followers_get(user_name):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        tweets = db.execute(
            '''
            SELECT 
                user_details.user_name, 
                user_details.display_name, 
                tweets.tweet_id, 
                tweets.tweet_text, 
                tweets.tweet_timestamp,
                tweet_images.image_name
            FROM tweets
            LEFT JOIN tweet_images ON tweets.tweet_id = tweet_images.tweet_id
            JOIN user_details ON tweets.user_name = user_details.user_name
            ORDER BY tweets.tweet_timestamp DESC;
            ''').fetchall()
        return tweets
    finally:
        db.close()

def validation_get_by_url(url):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        validation = json.dumps(db.execute(
            '''
            SELECT 
                users.user_id, 
                users.user_name,
                users.user_email,
                email_validations.validation_url, 
                email_validations.validation_code
            FROM users
            INNER JOIN email_validations 
            ON email_validations.user_email=users.user_email
            WHERE validation_url=:validation_url;
            ''', dict(validation_url=url)).fetchone())
        return json.loads(validation)
    finally:
        db.close()

def validation_get_by_email(email):
    try:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = dict_factory
        validation = json.dumps(db.execute(
            '''
            SELECT 
                users.user_id, 
                users.user_name,
                users.user_email,
                email_validations.validation_url, 
                email_validations.validation_code
            FROM users
            INNER JOIN email_validations 
            ON email_validations.user_email=users.user_email 
            WHERE users.user_email=?;
            ''', (email,)).fetchone())
        return json.loads(validation)
    finally:
        db.close()

# TODO less complex SQL query without including the user might be better
def validation_update_code(email, new_code):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute(
            '''
            UPDATE email_validations
            SET validation_code=:validation_code
            WHERE user_email IN (
                SELECT e.user_email FROM email_validations e
                INNER JOIN users u 
                ON (e.user_email=u.user_email)
                WHERE u.user_email=:email
            );
            ''', dict(email=email, validation_code=new_code))

        db.commit()
    finally:
        db.close()

def validation_delete(user):
    try:
        db = sqlite3.connect(DB_PATH)
        db.execute(
            '''
            DELETE FROM email_validations
            WHERE user_email IN (
                SELECT e.user_email FROM email_validations e
                INNER JOIN users u 
                ON (e.user_email=u.user_email)
                WHERE u.user_email=:user_email
            );
            ''', user)
        db.commit()
    finally:
        db.close()