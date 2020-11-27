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

    sql = "INSERT INTO messages (user_id, date_created, message) VALUES (:user_id, NOW(), :message)"
    db.session.execute(sql, {"user_id": user_id, "message": message})
    db.session.commit()
