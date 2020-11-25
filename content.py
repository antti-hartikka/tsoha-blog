from flask import make_response

import database
import accounts
from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy(app)


def create_new_post(username, title, post_type):
    user_id = accounts.get_user_id(username)
    sql = "INSERT INTO posts (user_id, post_type, title, date_created)" \
          "VALUES (:user_id, :type, :title, NOW()) " \
          "RETURNING id"
    result = db.session.execute(sql, {"user_id": user_id, "type": post_type, "title": title})
    db.session.commit()
    post_id = result.fetchone()[0]
    return post_id


def add_content(post_id, image_id, content_type, text):
    # get order number in post for content
    sql = "SELECT COUNT(*) " \
          "FROM postcontent " \
          "WHERE post_id=:post_id"
    result = db.session.execute(sql, {"post_id": post_id})
    order = result.fetchone()[0]

    # insert content info
    sql = "INSERT INTO content (image_id, media_text, media_type, order_number)" \
          "VALUES (:image_id, :text, :type, :order) " \
          "RETURNING id"
    result = db.session.execute(sql, {"image_id": image_id, "text": text, "type": content_type, "order": order})
    db.session.commit()

    # insert into postcontent
    content_id = result.fetchone()[0]
    sql = "INSERT INTO postcontent (post_id, content_id) " \
          "VALUES (:post_id, :content_id)"
    db.session.execute(sql, {"post_id": post_id, "content_id": content_id})
    db.session.commit()


# returns list of tuples containing posts
def get_posts(post_type):
    sql = "SELECT * " \
          "FROM posts " \
          "WHERE post_type=:post_type " \
          "ORDER BY date_created DESC"
    result = db.session.execute(sql, {"post_type": post_type})
    return result


# returns list of tuples containing content
def get_content(post_id):
    sql = "SELECT user_id, image_id, media_type, media_text " \
          "FROM content c " \
          "JOIN postcontent pc on c.id = pc.content_id " \
          "JOIN posts p on pc.post_id = p.id " \
          "WHERE p.id=:post_id " \
          "ORDER BY c.order_number ASC"
    result = db.session.execute(sql, {"post_id": post_id})
    return result


def modify_post(post_id, new_title):
    return True


def modify_content(content_id, new_content, new_alternative):
    return True


def add_image(file):
    name = file.filename
    if not name.endswith(".jpg") and not name.endswith(".jpeg") and not name.endswith(".png"):
        return "invalid filename"
    data = file.read()
    if len(data) > 500 * 1024:
        return "file too big"
    sql = "INSERT INTO images (name,data) " \
          "VALUES (:name,:data) " \
          "RETURNING id"
    result = db.session.execute(sql, {"name": name, "data": data})
    db.session.commit()
    image_id = result.fetchone()[0]
    return image_id


def get_image(id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response
