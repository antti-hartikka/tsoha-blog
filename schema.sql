CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    usergroup TEXT, -- basic, approved, admin
    is_active BOOLEAN
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    post_type TEXT,  -- short, long, private
    title TEXT,
    time_created TIMESTAMP,
    is_visible BOOLEAN
);

CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    name TEXT,
    data BYTEA);

CREATE TABLE content(
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images,
    media_text TEXT,
    media_type TEXT,  -- text, image
    order_number INTEGER
);

CREATE TABLE postcontent (
    post_id INTEGER REFERENCES posts,
    content_id INTEGER REFERENCES content
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    time_created TIMESTAMP,
    message TEXT
);

CREATE TABLE comments  (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    time_created TIMESTAMP,
    comment TEXT
);

INSERT INTO users (username) VALUES ('guest');