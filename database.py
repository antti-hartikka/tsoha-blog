from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy(app)


def get_user_count():
    sql = "SELECT COUNT(*) FROM users"
    result = db.session.execute(sql)
    count = result.fetchone()
    return count


def create_user(username, password, user_type):
    sql = "INSERT INTO users (username, password, user_type) VALUES (:username, :password, :user_type)"
    password_hash = generate_password_hash(password)
    db.session.execute(sql, {"username": username, "password": password_hash, "user_type": user_type})
    db.session.commit()


def check_credentials(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return False
    password_hash = user[0]
    if check_password_hash(password_hash, password):
        return True
    return False


def change_user_info(user, password, new_name, new_password, new_user_type):
    return False


def create_new_short_post(username, content):
    return False


def get_user_type(username):
    sql = "SELECT user_type FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    user_type = user[0]
    print("user_type: ", user_type)
    return user_type


def get_user_list():
    sql = "SELECT username FROM users"
    result = db.session.execute(sql)
    return result.fetchall()


def get_posts(string):
    return None