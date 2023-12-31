DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 title TEXT NOT NULL,
 content TEXT NOT NULL,
 tags TEXT ,
 coments TEXT
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username VARCHAR NOT NULL,
 pass VARCHAR NOT NULL,
 email VARCHAR NOT NULL
);
