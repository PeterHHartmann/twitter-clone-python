import mysql.connector
import json

db_config = {
  "host":"localhost",
  "port": 3306,
  "user":"root",
  "password":"",
  "database":"twitter_clone"
}

#db.sqlite3.connect
# db_conn = mysql.connector.connect(**db_config)
# Without dictionary = True it returns a multi-dimensional array
# [[1, "a", "@a"], [2, "b", "@b"]]
# db = db_conn.cursor(dictionary=True)
# print("*****")
# print(dir(db))
# print(' ')
# db.execute("SELECT * FROM users")
# users = db.fetchall()
# print(users)

db_conn = mysql.connector.connect(**db_config)


def user_insert(username, email, password):
    db = db_conn.cursor(dictionary=True)
    db.callproc('insert_new_user', [username, email, password])
    
    new_user = {}
    db.execute('SELECT @user_id')
    new_user['user_id'] = db.fetchone()['@user_id']
    db.execute('SELECT @url_snippet')
    new_user['url_snippet'] = db.fetchone()['@url_snippet']

    return new_user
