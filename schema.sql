CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    user_type TEXT -- basic, approved, admin
);

CREATE TABLE content(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    media_text TEXT,
    media_path TEXT,
    media_type TEXT,  -- text, image, video
    order_number INTEGER
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    post_type TEXT,  -- short, long, private
    title TEXT,
    date_created DATE,
    date_modified DATE
);

CREATE TABLE postcontent (
    post_id INTEGER REFERENCES posts,
    content_id INTEGER REFERENCES content
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    date_created DATE,
    message TEXT
);

CREATE TABLE comments  (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    post_id INTEGER REFERENCES posts,
    date_created DATE,
    comment TEXT
);