from app import app
from flask_sqlalchemy import SQLAlchemy

import accounts

db = SQLAlchemy(app)


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


