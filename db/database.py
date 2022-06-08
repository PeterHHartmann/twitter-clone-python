import mysql.connector

db_config = {
  "host":"localhost",
  "port": 3306,
  "user":"root",
  "password":"",
  "database":"twitter_clone"
}

db_conn = mysql.connector.connect(**db_config)
# db_conn.autocommit = False

def user_select_by_email(email):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT * 
      FROM users 
      WHERE email=%(email)s
    '''
    params = {'email': email}
    db.execute(query, params)
    user = db.fetchone()
    return user
  finally:
      db.close()

def user_select_by_username(user_name):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT * 
      FROM users 
      WHERE user_name = %(user_name)s
    '''
    params = {'user_name': user_name}
    db.execute(query, params)
    user = db.fetchone()
    return user
  finally:
      db.close()

def user_insert(username, email, password):
  try:
    db = db_conn.cursor(dictionary=True)
    db.callproc('insert_new_user', [username, email, password])
    new_user = {}
    db.execute('SELECT @user_id')
    new_user['user_id'] = db.fetchone()['@user_id']
    db.execute('SELECT @url_snippet')
    new_user['url_snippet'] = db.fetchone()['@url_snippet']
    return new_user
  finally:
    db.close()

def profile_select(user_name):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT
        u.user_name,
        up.user_id,
        up.display_name, 
        up.bio, 
        up.joined_at, 
        a.image_name AS avatar_image_name, 
        b.image_name AS banner_image_name
      FROM 
        users u,
        user_profiles up
      LEFT JOIN avatars a ON a.user_id = up.user_id
      LEFT JOIN banners b ON b.user_id = up.user_id
      WHERE u.user_name = %(user_name)s
      AND up.user_id = u.user_id
      AND NOT u.user_id IN (
        SELECT uv.user_id
        FROM user_verifications uv
        WHERE uv.user_id = u.user_id
      )
      LIMIT 1;
    '''
    params = {'user_name': user_name}
    db.execute(query, params)
    profile = db.fetchone()
    return profile
  finally:
    db.close()

def profile_update(user_id, display_name, bio):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      UPDATE user_profiles
      SET 
        display_name=%(display_name)s, 
        bio=%(bio)s
      WHERE user_id=%(user_id)s;
    '''
    params = {'user_id': user_id, 'display_name': display_name, 'bio': bio}
    db.execute(query, params)
    db_conn.commit()
    return
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def profiles_select_who_to_follow(user_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT 
        u.user_name, 
        up.display_name,
        a.image_name AS avatar_image_name, 
        b.image_name AS banner_image_name
      FROM 
        users u, 
        user_profiles up, 
        avatars a, 
        banners b
      WHERE NOT up.user_id = %(user_id)s
      AND NOT up.user_id = "admin"
      AND up.user_id = u.user_id
      AND a.user_id = u.user_id
      AND b.user_id = u.user_id
      AND NOT u.user_id IN (
        SELECT f.is_following 
        FROM follows f
        WHERE f.user_id = %(user_id)s
      )
      AND NOT u.user_id IN (
        SELECT uv.user_id
        FROM user_verifications uv
        WHERE uv.user_id = u.user_id
      )
      ORDER BY joined_at DESC 
      LIMIT 10;
    '''
    params = {'user_id': user_id}
    db.execute(query, params)
    profiles = db.fetchall()
    return profiles
  finally:
    db.close()

def avatar_select(user_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT
        image_name, 
        image_blob, 
        last_modified
      FROM avatars
      WHERE user_id=%(user_id)s
      LIMIT 1;
    '''
    params = {'user_id': user_id}
    db.execute(query, params)
    avatar = db.fetchone()
    return avatar
  finally:
    db.close()

def avatar_insert(user_id, image_name, image_blob):
  try:
    db = db_conn.cursor(buffered=True)
    query = '''
    INSERT INTO avatars(user_id, image_name, image_blob) 
    VALUES(%(user_id)s, %(image_name)s, %(image_blob)s);
    '''
    params = {'user_id': user_id, 'image_name': image_name, 'image_blob': image_blob}
    db.execute(query, params)
    db_conn.commit()
    return
  finally:
    db.close()

def avatar_update(user_id, image_name, image_blob):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      UPDATE avatars
      SET
      image_name=%(image_name)s,
      image_blob=%(image_blob)s
      WHERE user_id = %(user_id)s
    '''
    params = {'user_id': user_id, 'image_name': image_name, 'image_blob': image_blob}
    db.execute(query, params)
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
    raise error
  finally:
    db.close()

def banner_select(user_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT image_name, image_blob, last_modified
      FROM banners
      WHERE user_id=%(user_id)s
      LIMIT 1;
    '''
    params = {'user_id': user_id}
    db.execute(query, params)
    avatar = db.fetchone()
    return avatar
  finally:
    db.close()

def banner_insert(user_id, image_name, image_blob):
  try:
    db = db_conn.cursor(buffered=True)
    query = '''
    INSERT INTO banners(user_id, image_name, image_blob) 
    VALUES(%(user_id)s, %(image_name)s, %(image_blob)s);
    '''
    params = {'user_id': user_id, 'image_name': image_name, 'image_blob': image_blob}
    db.execute(query, params)
    db_conn.commit()
    return
  finally:
    db.close()

def banner_update(user_id, image_name, image_blob):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      UPDATE banners
      SET 
      image_name=%(image_name)s,
      image_blob=%(image_blob)s
      WHERE user_id=%(user_id)s;
    '''
    params = {'user_id': user_id, 'image_name': image_name, 'image_blob': image_blob}
    db.execute(query, params)
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def tweet_select(tweet_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT *
      FROM tweets t
      WHERE t.tweet_id=%(tweet_id)s;
    '''
    params = {'tweet_id': tweet_id}
    db.execute(query, params)
    tweet = db.fetchone()
    query = '''
      SELECT 
        ti.image_name
      FROM 
        tweet_images ti
      WHERE ti.tweet_id = %(tweet_id)s
      LIMIT 4;
    '''
    params = {'tweet_id': tweet['tweet_id']}
    db.execute(query, params)
    tweet_images = db.fetchall()
    tweet['images'] = tweet_images
    return tweet
  finally:
    db.close()

def tweet_insert(user_id, tweet):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      INSERT INTO tweets(user_id, tweet_text)
      VALUES(%(user_id)s, %(tweet_text)s)
    '''
    params = {'user_id': user_id, 'tweet_text': tweet['text']}
    db.execute(query, params)
    if tweet.get('images'):
      tweet_id = db.lastrowid
      for tweet_image in tweet['images']:
        image_query = '''
          INSERT INTO tweet_images(tweet_id, image_name, image_blob)
          VALUES(%(tweet_id)s, %(image_name)s, %(image_blob)s);
        '''
        image_params = {'tweet_id': tweet_id, 'image_name': tweet_image['image_name'], 'image_blob': tweet_image['image_blob']}
        db.execute(image_query, image_params)
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def tweet_update(tweet_id, tweet_text):
  try:
      db = db_conn.cursor(dictionary=True)
      query = '''
        UPDATE tweets
        SET tweet_text=%(tweet_text)s
        WHERE tweet_id=%(tweet_id)s;
      '''
      params = {'tweet_id': tweet_id, 'tweet_text': tweet_text}
      db.execute(query, params)
      db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()


def tweet_delete(tweet_id):
  try:
      db = db_conn.cursor(dictionary=True)
      query = '''
        DELETE FROM tweets
        WHERE tweet_id=%(tweet_id)s;
      '''
      params = {'tweet_id': tweet_id}
      db.execute(query, params)
      db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def tweets_select_by_user(user_name):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT 
        t.tweet_id, 
        t.tweet_text, 
        t.created_at,
        u.user_id,
        u.user_name,
        up.display_name, 
        a.image_name AS avatar_image_name
      FROM 
        tweets t
      JOIN user_profiles up ON up.user_id = t.user_id
      JOIN users u ON u.user_id = t.user_id
      LEFT JOIN avatars a ON a.user_id = t.user_id
      WHERE u.user_name = %(user_name)s
      ORDER BY t.created_at DESC
      LIMIT 10;
    '''
    params = {'user_name': user_name}
    db.execute(query, params)
    tweets = db.fetchall()
    for tweet in tweets:
      query = '''
        SELECT 
          ti.image_name
        FROM 
          tweet_images ti
        WHERE ti.tweet_id = %(tweet_id)s
        LIMIT 4;
      '''
      params = {'tweet_id': tweet['tweet_id']}
      db.execute(query, params)
      tweet_images = db.fetchall()
      tweet['images'] = tweet_images
    return tweets
  finally:
    db.close()

def tweets_select_by_following(user_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT
        t.tweet_id, 
        t.tweet_text, 
        t.created_at,
        u.user_id,
        u.user_name, 
        up.display_name,
        a.image_name AS avatar_image_name
      FROM 
        tweets t
      JOIN users u ON u.user_id = t.user_id
      JOIN user_profiles up ON up.user_id = u.user_id
      LEFT JOIN avatars a ON a.user_id = up.user_id
      WHERE u.user_id IN (
        SELECT f.is_following
        FROM follows f
        WHERE f.user_id = %(user_id)s
      ) OR t.user_id = %(user_id)s
      ORDER BY t.created_at DESC
      LIMIT 10;
    '''
    params = {'user_id': user_id}
    db.execute(query, params)
    tweets = db.fetchall()
    for tweet in tweets:
      query = '''
        SELECT 
          ti.image_name
        FROM 
          tweet_images ti
        WHERE ti.tweet_id = %(tweet_id)s
        LIMIT 4;
      '''
      params = {'tweet_id': tweet['tweet_id']}
      db.execute(query, params)
      tweet_images = db.fetchall()
      tweet['images'] = tweet_images
    return tweets
  finally:
    db.close()

def tweets_select_all():
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT
        t.tweet_id, 
        t.tweet_text, 
        t.created_at,
        u.user_id,
        u.user_name, 
        up.display_name,
        a.image_name AS avatar_image_name
      FROM 
        tweets t
      JOIN users u ON u.user_id = t.user_id
      JOIN user_profiles up ON up.user_id = u.user_id
      LEFT JOIN avatars a ON a.user_id = up.user_id
      ORDER BY t.created_at DESC
      LIMIT 10;
    '''
    db.execute(query)
    tweets = db.fetchall()
    for tweet in tweets:
      query = '''
        SELECT 
          ti.image_name
        FROM 
          tweet_images ti
        WHERE ti.tweet_id = %(tweet_id)s
        LIMIT 4;
      '''
      params = {'tweet_id': tweet['tweet_id']}
      db.execute(query, params)
      tweet_images = db.fetchall()
      tweet['images'] = tweet_images
    return tweets
  finally:
      db.close()

def tweet_image_select(image_name):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT 
        tweet_id, 
        image_name, 
        image_blob
      FROM tweet_images
      WHERE image_name=%(image_name)s
      LIMIT 1
    '''
    params = {'image_name': image_name}
    db.execute(query, params)
    image = db.fetchone()
    return image
  finally:
      db.close()

def follow_insert(user_id, user_name_to_follow):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT users.user_id 
      FROM users 
      WHERE users.user_name = %(user_name)s 
      LIMIT 1
    '''
    params = {'user_name': user_name_to_follow}
    db.execute(query, params)
    is_following = db.fetchone()
    query = '''
      INSERT INTO follows(user_id, is_following)
      VALUES(%(user_id)s, %(is_following)s);
    '''
    params = {'user_id': user_id, 'is_following': is_following['user_id']}
    db.execute(query, params)
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def follow_delete(user_id, user_name_to_follow):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT users.user_id 
      FROM users 
      WHERE users.user_name = %(user_name)s 
      LIMIT 1
    '''
    params = {'user_name': user_name_to_follow}
    db.execute(query, params)
    is_following = db.fetchone()
    query = '''
      DELETE FROM follows
      WHERE user_id = %(user_id)s
      AND is_following = %(is_following)s;
    '''
    params = {'user_id': user_id, 'is_following': is_following['user_id']}
    db.execute(query, params)
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def follow_select(user_id, user_name_to_follow):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT u.user_id 
      FROM users u
      WHERE u.user_name = %(user_name)s 
      LIMIT 1
    '''
    params = {'user_name': user_name_to_follow}
    db.execute(query, params)
    is_following = db.fetchone()
    query = '''
      SELECT f.is_following 
      FROM follows f
      WHERE f.user_id = %(user_id)s
      AND f.is_following = %(is_following)s
      LIMIT 1;
    '''
    params = {'user_id': user_id, 'is_following': is_following['user_id']}
    db.execute(query, params)
    is_following = db.fetchone()
    return is_following
  finally:
    db.close()

def verification_select_by_url_snippet(url_snippet):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT 
        u.user_id, 
        u.user_name,
        u.email,
        uv.url_snippet, 
        uv.verification_code
      FROM users u
      INNER JOIN user_verifications uv
      ON uv.user_id = u.user_id
      WHERE uv.url_snippet=%(url_snippet)s;
    '''
    params = {'url_snippet': url_snippet}
    db.execute(query, params)
    user_verification = db.fetchone()
    return user_verification
  finally:
    db.close()

def verification_select_by_user_id(user_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      SELECT 
        u.user_id, 
        u.user_name,
        u.email,
        uv.url_snippet, 
        uv.verification_code
      FROM users u
      INNER JOIN user_verifications uv
      ON uv.user_id = u.user_id
      WHERE u.user_id=%(user_id)s;
    '''
    params = {'user_id': user_id}
    db.execute(query, params)
    user_verification = db.fetchone()
    return user_verification
  finally:
    db.close()

def verification_update_code(user_id, new_code):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      UPDATE user_verifications
      SET verification_code = %{new_code}s
      WHERE user_id IN (
          SELECT uv.user_id FROM user_verifications uv
          INNER JOIN users u 
          ON uv.user_id = u.user_id
          WHERE u.user_id=%(user_id)s
      );
    '''
    params = {'user_id': user_id, 'new_code': new_code}
    db.execute(query, params)
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

def verification_delete(user_id):
  try:
    db = db_conn.cursor(dictionary=True)
    query = '''
      DELETE FROM user_verifications
      WHERE user_id IN (
          SELECT uv.user_id FROM user_verifications uv
          INNER JOIN users u 
          ON uv.user_id = u.user_id
          WHERE u.user_id=%(user_id)s
      );
    '''
    params = {'user_id': user_id}
    db.execute(query, params) 
    db_conn.commit()
  except mysql.connector.Error as error:
    print("Failed to update record to database rollback: {}".format(error))
    db_conn.rollback()
  finally:
    db.close()

# verification_select_by_user_id('4fdd30e4-e695-11ec-ad88-2cf05d0b549f')
# tweets_select_by_user('barackobama')

# tweet_insert('be66f1a6-e143-11ec-ab61-2cf05d0b549f', {'text':'hi', 'images': [{'image_name': "test1"}, {'image_name': "test2"}]})
# tweet_insert('be66f1a6-e143-11ec-ab61-2cf05d0b549f', {'text': 'hi2'})
# barackobama = be66f1a6-e143-11ec-ab61-2cf05d0b549f

# kendricklamar = be67b113-e143-11ec-ab61-2cf05d0b549f