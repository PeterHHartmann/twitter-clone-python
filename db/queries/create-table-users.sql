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
    joined_date             REAL NOT NULL,
    CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES users(user_name),
    PRIMARY KEY (detail_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS profile_pictures;
CREATE TABLE profile_pictures (
    image_id                INTEGER NOT NULL,
    user_name               TEXT NOT NULL,
    image_name              TEXT,
    image_blob              BLOB,
    last_modified           REAL NOT NULL,
    PRIMARY KEY (image_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS banners;
CREATE TABLE banners (
    image_id                INTEGER NOT NULL,
    user_name               TEXT NOT NULL,
    image_name              TEXT,
    image_blob              BLOB,
    last_modified           REAL NOT NULL,
    PRIMARY KEY (image_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS tweets;
CREATE TABLE tweets (
    tweet_id                INTEGER NOT NULL,
    user_name               TEXT NOT NULL,
    tweet_text              TEXT NOT NULL,
    tweet_img               BLOB,
    tweet_timestamp         REAL NOT NULL,
    CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES user_details(user_name),
    PRIMARY KEY (tweet_id AUTOINCREMENT)
);

DROP TABLE IF EXISTS follows;
CREATE TABLE follows (
    user_name               TEXT NOT NULL,
    follows_user            TEXT NOT NULL,
    CONSTRAINT fk_user_name FOREIGN KEY (user_name) REFERENCES users(user_name),
    PRIMARY KEY (user_name, follows_user)
);

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('Tom', 'test@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');
INSERT INTO user_details(user_name, display_name, bio, joined_date) 
VALUES('Tom', 'Tom From Myspace', "hi it's me Tom!", 1650719171.8843205);
INSERT INTO profile_pictures(user_name, last_modified) 
VALUES('Tom', 1650719171.8843205);
INSERT INTO banners(user_name, last_modified) 
VALUES('Tom', 1650719171.8843205);

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('jack', 'jack@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');
INSERT INTO user_details(user_name, display_name, joined_date) 
VALUES('jack', 'jack', 1650719171.8843205);
INSERT INTO profile_pictures(user_name, last_modified) 
VALUES('jack', 1650719171.8843205);
INSERT INTO banners(user_name, last_modified) 
VALUES('jack', 1650719171.8843205);

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('barackobama', 'barackobama@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');
INSERT INTO user_details(user_name, display_name, bio, joined_date) 
VALUES('barackobama', 'Barack Obama', "Former President of The United States", 1650719171.8843205);
INSERT INTO profile_pictures(user_name, last_modified) 
VALUES('barackobama', 1650719171.8843205);
INSERT INTO banners(user_name, last_modified) 
VALUES('barackobama', 1650719171.8843205);

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('elonmusk', 'elonmusk@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');
INSERT INTO user_details(user_name, display_name, bio, joined_date) 
VALUES('elonmusk', 'Elon Musk', "Owner of Tesla, SpaceX and Twitter", 1650719171.8843205);
INSERT INTO profile_pictures(user_name, last_modified) 
VALUES('elonmusk', 1650719171.8843205);
INSERT INTO banners(user_name, last_modified) 
VALUES('elonmusk', 1650719171.8843205);

INSERT INTO users(user_name, user_email, user_pwd) 
VALUES('kendricklamar', 'kendricklamar@email.com', '$2b$12$r1XwsYlYdoqf7GC3i256aOajRcJ3AbWlUOPUJuERhJVUExKzH9Hq6');
INSERT INTO user_details(user_name, display_name, bio, joined_date) 
VALUES('kendricklamar', 'Kung Fu Kenny', "Grammy award winning musician", 1650719171.8843205);
INSERT INTO profile_pictures(user_name, last_modified) 
VALUES('kendricklamar', 1650719171.8843205);
INSERT INTO banners(user_name, last_modified) 
VALUES('kendricklamar', 1650719171.8843205);

INSERT INTO follows(user_name, follows_user)
VALUES('Tom','jack');
INSERT INTO follows(user_name, follows_user)
VALUES('Tom','barackobama');
INSERT INTO follows(user_name, follows_user)
VALUES('Tom','elonmusk');
INSERT INTO follows(user_name, follows_user)
VALUES('Tom','kendricklamar');

INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
VALUES('jack', 'I made the original...', 1651170736.8599896);

INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
VALUES('barackobama', 'Personally a big fan of Kendrick Lamar', 1651160236.8599896);

INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
VALUES('elonmusk', 'I own this place now!', 1651060236.8599896);

INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
VALUES('kendricklamar', 'New album dropping soon', 1651170936.8599896);

INSERT INTO tweets(user_name, tweet_text, tweet_timestamp)
VALUES('Tom', 'MySpace was way better, right guys?', 1651000836.8599896);
