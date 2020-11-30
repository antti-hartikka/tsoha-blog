import database
from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import re


db = SQLAlchemy(app)


# if username validation is not ok, returns "username not ok"
# if username already exists, returns "username taken"
# if password validation is not ok, returns "password not ok"
# otherwise creates new user into database and returns "ok"
def create_user(username, password):
    if not validate_username(username):
        return "username not ok"
    if user_exists(username):
        return "username taken"
    if not validate_password(password):
        return "password not ok"
    sql = "INSERT INTO users (username, password, usergroup, is_active) " \
          "VALUES (:username, :password, 'basic', TRUE)"
    password_hash = generate_password_hash(password)
    db.session.execute(sql, {"username": username, "password": password_hash})
    db.session.commit()
    return "ok"


# returns true if username matches password in database, returns false if validation returns false or user doesn't exist
def check_credentials(username, password):
    if not validate_username(username) or not validate_password(password):
        return False
    sql = "SELECT password " \
          "FROM users " \
          "WHERE username=:username AND is_active=TRUE"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return False
    password_hash = user[0]
    if check_password_hash(password_hash, password):
        return True
    return False


# returns "username not ok" if in incorrect form, "username taken" if username is taken and "ok" if updated
def set_username(old_name, new_name):
    if not validate_username(new_name):
        return "username not ok"
    if user_exists(new_name):
        return "username taken"
    sql = "UPDATE users " \
          "SET username=:new " \
          "WHERE username=:old"
    db.session.execute(sql, {"new": new_name, "old": old_name})
    db.session.commit()
    return "ok"


# returns "bad password" if password validation is not ok, otherwise returns "ok"
def set_password(username, new_password):
    if not validate_password(new_password):
        return "bad password"
    new_password_hash = generate_password_hash(new_password)
    sql = "UPDATE users " \
          "SET password=:new_pw " \
          "WHERE username=:username"
    db.session.execute(sql, {"new_pw": new_password_hash, "username": username})
    db.session.commit()
    return "ok"


def set_usergroup(username, usergroup):
    sql = "UPDATE users " \
          "SET usergroup=:new_group " \
          "WHERE username=:username"
    db.session.execute(sql, {"new_group": usergroup, "username": username})
    db.session.commit()


def get_usergroup(username):
    sql = "SELECT usergroup " \
          "FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return ""
    usergroup = user[0]
    return usergroup


def get_user_list():
    sql = "SELECT username " \
          "FROM users " \
          "WHERE is_active"
    result = db.session.execute(sql)
    return result.fetchall()


# Returns true if database contains user
def user_exists(username):
    sql = "SELECT username " \
          "FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return False
    else:
        return True


# set user type to basic, set password to "deleted", set username to "[deleted]", set is_active to FALSE
def delete_account(username):
    set_usergroup(username, "basic")
    password = generate_password_hash("deleted")
    set_password(username, password)
    sql = "UPDATE users " \
          "SET is_active=FALSE, username='[deleted]' " \
          "WHERE username=:username"
    db.session.execute(sql, {"username": username})
    db.session.commit()


# returns -1 if user not found
def get_user_id(username):
    if not user_exists(username):
        return -1
    sql = "SELECT id " \
          "FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user_id = result.fetchone()[0]
    return user_id


# returns true if username is 3-20 characters long and consists of letters and numbers
def validate_username(username):
    if re.match(r"^[a-zA-Z0-9]{3,20}$", username):
        return True
    return False


# returns true if password is 10-30 characters long and consists of letters and numbers
def validate_password(password):
    if re.match(r"^[a-zA-Z0-9]{10,30}$", password):
        return True
    return False
