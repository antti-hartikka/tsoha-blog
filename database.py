from app import app
from flask_sqlalchemy import SQLAlchemy

import accounts

db = SQLAlchemy(app)


def file_input(file):
    name = file.filename
    if not name.endswith(".jpg"):
        return "Invalid filename"
    data = file.read()
    if len(data) > 500 * 1024:
        return "Too big file"
    return data


def insert_message(username, message):
    user_id = accounts.get_user_id(username)

    sql = "INSERT INTO messages (user_id, time_created, message) VALUES (:user_id, NOW(), :message)"
    db.session.execute(sql, {"user_id": user_id, "message": message})
    db.session.commit()


def get_messages():
    sql = "SELECT m.id, u.username, m.message, m.time_created FROM messages m " \
          "JOIN users u on m.user_id = u.id " \
          "ORDER BY m.time_created"
    result = db.session.execute(sql)
    message_list = result.fetchall()
    return message_list


def delete_message(message_id):
    sql = "DELETE FROM messages WHERE id = :id"
    db.session.execute(sql, {"id": message_id})
    db.session.commit()


def get_comments(post_id):
    sql = "SELECT c.time_created, u.username, c.comment FROM comments c " \
          "JOIN users u on u.id = c.user_id " \
          "WHERE post_id=:post_id"
    result = db.session.execute(sql, {"post_id": post_id})
    comments = result.fetchall()
    return comments


def insert_comment(username, post_id, comment):
    user_id = accounts.get_user_id(username)
    sql = "INSERT INTO comments (user_id, post_id, time_created, comment) " \
          "VALUES (:user_id, :post_id, now(), :comment)"
    db.session.execute(sql, {"user_id": user_id, "post_id": post_id, "comment": comment})
    db.session.commit()
