DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id                 INTEGER NOT NULL,
    user_name               TEXT UNIQUE NOT NULL,
    user_email              TEXT UNIQUE NOT NULL,
    user_pwd                TEXT NOT NULL,
    PRIMARY KEY(user_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS email_validations;
CREATE TABLE email_validations (
	validation_id	        INTEGER NOT NULL,
	user_email	            TEXT UNIQUE NOT NULL,
    validation_url          TEXT UNIQUE NOT NULL,
	validation_code	        INTEGER NOT NULL,
	CONSTRAINT fk_user_email FOREIGN KEY (user_email) REFERENCES users(user_email),
	PRIMARY KEY (validation_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS user_details;
CREATE TABLE user_details (
    detail_id               INTEGER NOT NULL,
    user_name               TEXT UNIQUE NOT NULL,
    display_name            TEXT NOT NULL,
    bio                     TEXT,
    pfp                     BLOB,
    banner                  BLOB,
    joined_date             REAL NOT NULL,
    CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES users(user_name),
    PRIMARY KEY (detail_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS users_tweets;
CREATE TABLE users_tweets (
    tweet_id                INTEGER NOT NULL,
    user_name               TEXT NOT NULL,
    CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES user_details(user_name),
    CONSTRAINT fk_tweet_id  FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
);

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
    tweet_id                INTEGER NOT NULL,
    tweet_text              TEXT NOT NULL,
    tweet_img               BLOB,
    tweet_timestamp         REAL NOT NULL,
    PRIMARY KEY (tweet_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS follows;
CREATE TABLE follows (
    user_name               TEXT NOT NULL,
    follows_user            TEXT NOT NULL,
    CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES users(user_name),
    PRIMARY KEY (user_name, follows_user)
);


-- ALTER TABLE users
-- ADD FOREIGN KEY (user_id) REFERENCES confirmations(user_id)

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('Tom', 'test@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');

INSERT INTO user_details(user_name, display_name, bio, joined_date) 
VALUES('Tom', 'Tom From Myspace', "hi it's me Tom!", 1650719171.8843205);

-- INSERT INTO tweets(tweet_text, tweet_timestamp)
-- VALUES('This is a test tweet', 1650719171.8843205);

-- INSERT INTO users_tweets(user_name, tweet_id)
-- VALUES('Tom', last_insert_rowid());

-- INSERT INTO tweets(tweet_text, tweet_timestamp)
-- VALUES('This is a 2nd test tweet', 1650719171.8843205);

-- INSERT INTO users_tweets(user_name, tweet_id)
-- VALUES('Tom2', last_insert_rowid());

-- INSERT INTO tweets(tweet_text, tweet_timestamp)
-- VALUES('This is a 3rd test tweet', 1650719171.8843205);

-- INSERT INTO users_tweets(user_name, tweet_id)
-- VALUES('Tom2', last_insert_rowid());

-- INSERT INTO follows(user_name, follows_user)
-- VALUES('Tom', 'Tom2');

-- SELECT users.user_id, users.user_name, users.user_email, users.user_pwd, email_validations.validation_url, email_validations.validation_code
-- FROM users
-- INNER JOIN email_validations ON email_validations.user_id=users.user_id WHERE validation_url="dd12293c-a47d-4541-bc97-4de2e1e544c6";