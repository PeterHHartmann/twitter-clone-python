import psycopg2
import psycopg2.extras

db_config = {
  "host":"localhost",
  "port": 5432,
  "user":"peterhartmann",
  "database":"twitter-clone"
}

def user_get_by_email(user_email):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT * 
            FROM users 
            WHERE user_email=%(user_email)s;
            ''', dict(user_email=user_email))
        user = cursor.fetchone()
        return user
    finally:
        conn.close()

def user_get_by_username(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT * 
            FROM users 
            WHERE user_name=%(user_name)s;
        ''', dict(user_name=user_name))
        user = cursor.fetchone()
        return user
    finally:
        conn.close()

def user_post(user, details):
  try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('''
        INSERT INTO users(user_name, user_email, user_pwd) 
        VALUES(%(user_name)s, %(user_email)s, %(user_pwd)s);
        ''', user)
    cursor.execute('''
        INSERT INTO user_details(user_name, display_name, joined_date) 
        VALUES(%(user_name)s, %(display_name)s, %(joined_date)s);
        ''', dict(user_name=user['user_name'], display_name=user['user_name'], **details))
    cursor.execute('''
        INSERT INTO profile_pictures(user_name, last_modified) 
        VALUES(%(user_name)s, %(last_modified)s);
        ''', dict(user_name=user['user_name'], last_modified=details['joined_date']))
    cursor.execute('''
        INSERT INTO banners(user_name, last_modified) 
        VALUES(%(user_name)s, %(last_modified)s);
        ''', dict(user_name=user['user_name'], last_modified=details['joined_date']))
    conn.commit()
  finally:
    conn.close()

#TODO get users with the most followers once implemented
def details_get_who_to_follow(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT 
                u.user_name, 
                ud.display_name,
                pp.image_name AS pfp_image_name, 
                b.image_name AS banner_image_name
            FROM 
                users u, 
                user_details ud, 
                profile_pictures pp, 
                banners b
            WHERE NOT ud.user_name = %(user_name)s
            AND ud.user_name = u.user_name
            AND pp.user_name = u.user_name
            AND b.user_name = u.user_name
            AND NOT u.user_name IN (
                SELECT f.follows_user 
                FROM follows f
                WHERE f.user_name = %(user_name)s
            )
            AND NOT u.user_email IN (
                SELECT e.user_email
                FROM email_validations e
                WHERE e.user_email = u.user_email
            )
            ORDER BY joined_date DESC 
            LIMIT 10;
        ''', dict(user_name = user_name))
        users = cursor.fetchall()
        return users
    finally:
        conn.close()

def details_get(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT
                u.user_name, 
                ud.display_name, 
                ud.bio, 
                ud.joined_date, 
                pp.image_name AS pfp_image_name, 
                b.image_name AS banner_image_name
            FROM 
                users u, 
                user_details ud, 
                profile_pictures pp, 
                banners b
            WHERE u.user_name = %(user_name)s
            AND ud.user_name = u.user_name
            AND pp.user_name = u.user_name
            AND b.user_name = u.user_name
            AND NOT u.user_email IN (
                SELECT e.user_email
                FROM email_validations e
                WHERE e.user_email = u.user_email
            )
            LIMIT 1;
            ''', dict(user_name=user_name))
        details = cursor.fetchone()
        return details
    finally:
        conn.close()

def details_update(user_name, details):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            UPDATE user_details
            SET 
            display_name=%(display_name)s, 
            bio=%(bio)s
            WHERE user_name=%(user_name)s;
            ''', dict(user_name=user_name, **details))
        conn.commit()
    finally:
        conn.close()

def profile_picture_get(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT image_name, image_blob, last_modified
            FROM profile_pictures
            WHERE user_name=%(user_name)s
            LIMIT 1
            ''', dict(user_name=user_name))
        profile_picture = cursor.fetchone()
        return profile_picture
    finally:
        conn.close()

def profile_picture_update(user_name, profile_picture):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            UPDATE profile_pictures
            SET 
            image_name=%(image_name)s, 
            image_blob=%(image_blob)s, 
            last_modified=%(last_modified)s
            WHERE user_name=%(user_name)s;
            ''', dict(user_name=user_name, **profile_picture))
        conn.commit()
    finally:
        conn.close()

def banner_get(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT image_name, image_blob, last_modified
            FROM banners
            WHERE user_name=%(user_name)s
            ''', dict(user_name=user_name))
        profile_picture = cursor.fetchone()
        return profile_picture
    finally:
        conn.close()

def banner_update(user_name, banner):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            UPDATE banners
            SET 
            image_name=%(image_name)s, 
            image_blob=%(image_blob)s, 
            last_modified=%(last_modified)s
            WHERE user_name=%(user_name)s;
            ''', dict(user_name=user_name, **banner))
        conn.commit()
    finally:
        conn.close()

def tweet_get(tweet_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT *
            FROM tweets
            WHERE tweet_id=%(tweet_id)s
            ''', dict(tweet_id=tweet_id))
        content = cursor.fetchone()
        return content
    finally:
        conn.close()

def tweet_post(user_name, tweet):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
            VALUES(%(user_name)s, %(tweet_text)s, %(tweet_timestamp)s)
            ''', dict(user_name=user_name, **tweet))
        tweet_id = cursor.lastrowid
        if tweet.get('image_blob'):
            cursor.execute('''
                INSERT INTO tweet_images(tweet_id, image_name, image_blob)
                VALUES(%(tweet_id)s, %(image_name)s, %(image_blob)s)
            ''', dict(tweet_id=tweet_id, image_name=tweet['image_name'], image_blob=tweet['image_blob']))
        conn.commit()
        return tweet_id
    finally:
        conn.close()

def tweet_get_image(tweet_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            SELECT 
                tweet_id, 
                image_name, 
                image_blob
            FROM tweet_images
            WHERE tweet_id=%(tweet_id)s
            ''', dict(tweet_id=tweet_id))
        content = cursor.fetchone()
        return content
    finally:
        conn.close()

def tweet_update(tweet_id, tweet_text):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            UPDATE tweets
            SET tweet_text=%(tweet_text)s
            WHERE tweet_id=%(tweet_id)s;
            ''', dict(tweet_text=tweet_text, tweet_id=tweet_id))
        conn.commit()
    finally:
        conn.close()

def tweet_delete(tweet_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            DELETE FROM tweet_images
            WHERE tweet_id=%(tweet_id)s;
            ''', dict(tweet_id=tweet_id))
        cursor.execute(
            '''
            DELETE FROM tweets
            WHERE tweet_id=%(tweet_id)s;
            ''', dict(tweet_id=tweet_id))
        conn.commit()
    finally:
        conn.close()

def tweets_get_by_user(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            SELECT 
                t.tweet_id, 
                t.tweet_text, 
                t.tweet_timestamp,
                ti.image_name,
                ud.user_name,
                ud.display_name, 
                pp.image_name AS pfp_image_name
            FROM 
                tweets t
            JOIN user_details ud ON ud.user_name = t.user_name
            LEFT JOIN profile_pictures pp ON pp.user_name = t.user_name
            LEFT JOIN tweet_images ti ON ti.tweet_id = t.tweet_id
            WHERE t.user_name = %(user_name)s
            ORDER BY t.tweet_timestamp DESC
            LIMIT 10;
            ''', dict(user_name=user_name))

        tweets = cursor.fetchall()
        return tweets
    finally:
        conn.close()

def tweets_get_following(user_name):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            SELECT
                t.tweet_id, 
                t.tweet_text, 
                t.tweet_timestamp,
                ti.image_name,
                ud.user_name, 
                ud.display_name,
                pp.image_name AS pfp_image_name
            FROM 
                tweets t
            JOIN user_details ud ON ud.user_name = t.user_name
            LEFT JOIN profile_pictures pp ON pp.user_name = t.user_name
            LEFT JOIN tweet_images ti ON ti.tweet_id = t.tweet_id
            WHERE t.user_name IN (
                SELECT f.follows_user
                FROM follows f
                WHERE f.user_name = %(user_name)s
            ) OR t.user_name = %(user_name)s
            ORDER BY t.tweet_timestamp DESC
            LIMIT 10;
            ''', dict(user_name=user_name))
        tweets = cursor.fetchall()
        return tweets
    finally:
        conn.close()

def tweets_get_all():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            SELECT
                t.tweet_id, 
                t.tweet_text, 
                t.tweet_timestamp,
                ti.image_name,
                ud.user_name, 
                ud.display_name,
                pp.image_name AS pfp_image_name
            FROM 
                tweets t
            JOIN user_details ud ON ud.user_name = t.user_name
            LEFT JOIN profile_pictures pp ON pp.user_name = t.user_name
            LEFT JOIN tweet_images ti ON ti.tweet_id = t.tweet_id
            ORDER BY t.tweet_timestamp DESC;
            ''')
        tweets = cursor.fetchall()
        return tweets
    finally:
        conn.close()

def follow_post(user_name, follows_user):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('''
            INSERT INTO follows(user_name, follows_user)
            VALUES(%(user_name)s, %(follows_user)s)
        ''', dict(user_name=user_name, follows_user=follows_user))
        conn.commit()
    finally:
        conn.close()

def follow_delete(user_name, follows_user):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            DELETE FROM follows
            WHERE user_name = %(user_name)s
            AND follows_user = %(follows_user)s;
            ''', dict(user_name=user_name, follows_user=follows_user))
        conn.commit()
    finally:
        conn.close()

def is_following_get(user_name, follows_user):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            '''
            SELECT 
                follows_user
            FROM follows
            WHERE user_name = %(user_name)s
            AND follows_user = %(follows_user)s
            LIMIT 1;
            ''', dict(user_name=user_name, follows_user=follows_user))
        follows = cursor.fetchone()
        return follows
    finally:
        conn.close()

# def validation_get_by_url(url):
#     try:
#         db = sqlite3.connect(DB_PATH)
#         db.row_factory = dict_factory
#         validation = json.dumps(db.execute(
#             '''
#             SELECT 
#                 users.user_id, 
#                 users.user_name,
#                 users.user_email,
#                 email_validations.validation_url, 
#                 email_validations.validation_code
#             FROM users
#             INNER JOIN email_validations 
#             ON email_validations.user_email=users.user_email
#             WHERE validation_url=:validation_url;
#             ''', dict(validation_url=url)).fetchone())
#         return json.loads(validation)
#     finally:
#         db.close()

# def validation_get_by_email(email):
#     try:
#         db = sqlite3.connect(DB_PATH)
#         db.row_factory = dict_factory
#         validation = json.dumps(db.execute(
#             '''
#             SELECT 
#                 users.user_id, 
#                 users.user_name,
#                 users.user_email,
#                 email_validations.validation_url, 
#                 email_validations.validation_code
#             FROM users
#             INNER JOIN email_validations 
#             ON email_validations.user_email=users.user_email 
#             WHERE users.user_email=?;
#             ''', (email,)).fetchone())
#         return json.loads(validation)
#     finally:
#         db.close()

# # TODO less complex SQL query without including the user might be better
# def validation_update_code(email, new_code):
#     try:
#         db = sqlite3.connect(DB_PATH)
#         db.execute(
#             '''
#             UPDATE email_validations
#             SET validation_code=:validation_code
#             WHERE user_email IN (
#                 SELECT e.user_email FROM email_validations e
#                 INNER JOIN users u 
#                 ON (e.user_email=u.user_email)
#                 WHERE u.user_email=:email
#             );
#             ''', dict(email=email, validation_code=new_code))

#         db.commit()
#     finally:
#         db.close()

# def validation_delete(user):
#     try:
#         db = sqlite3.connect(DB_PATH)
#         db.execute(
#             '''
#             DELETE FROM email_validations
#             WHERE user_email IN (
#                 SELECT e.user_email FROM email_validations e
#                 INNER JOIN users u 
#                 ON (e.user_email=u.user_email)
#                 WHERE u.user_email=:user_email
#             );
#             ''', user)
#         db.commit()
#     finally:
#         db.close()