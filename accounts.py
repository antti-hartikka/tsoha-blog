from werkzeug.security import check_password_hash, generate_password_hash
import re
from app import db


def create_user(username, password):
    """Returns "ok" if new user is created, otherwise returns error message string"""
    if not validate_username(username):
        return "käyttäjänimi on väärää muotoa"
    if user_exists(username):
        return "käyttäjänimi on jo käytössä"
    if not validate_password(password):
        return "salasana on väärää muotoa"
    sql = "INSERT INTO users (username, password, user_group, is_active) " \
          "VALUES (:username, :password, 'basic', TRUE)"
    password_hash = generate_password_hash(password)
    db.session.execute(sql, {"username": username, "password": password_hash})
    db.session.commit()
    return "ok"


def check_credentials(username, password):
    """returns true if username matches password in database,
    returns false if validation returns false or user doesn't exist"""
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


def set_username(old_name, new_name):
    """returns ok if username is updated, otherwise returns error message"""
    if not validate_username(new_name):
        return "käyttäjänimi on väärää muotoa"
    if user_exists(new_name):
        return "käyttäjänimi on jo käytössä"
    sql = "UPDATE users " \
          "SET username=:new " \
          "WHERE username=:old"
    db.session.execute(sql, {"new": new_name, "old": old_name})
    db.session.commit()
    return "ok"


def set_password(username, new_password):
    """returns "ok" if password is updated, otherwise returns error message"""
    if not validate_password(new_password):
        return "salasana on väärää muotoa"
    new_password_hash = generate_password_hash(new_password)
    sql = "UPDATE users " \
          "SET password=:new_pw " \
          "WHERE username=:username"
    db.session.execute(sql, {"new_pw": new_password_hash, "username": username})
    db.session.commit()
    return "ok"


def set_user_group(username, user_group):
    sql = "UPDATE users " \
          "SET user_group=:new_group " \
          "WHERE username=:username"
    db.session.execute(sql, {"new_group": user_group, "username": username})
    db.session.commit()


def get_user_group(username):
    """Returns user group as a string"""
    sql = "SELECT user_group " \
          "FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return ""
    user_group = user[0]
    return user_group


def get_user_list():
    sql = "SELECT username " \
          "FROM users " \
          "WHERE is_active"
    result = db.session.execute(sql)
    return result.fetchall()


def user_exists(username):
    """Returns true if database contains user"""
    sql = "SELECT username " \
          "FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if user is None:
        return False
    else:
        return True


def delete_account(username):
    """Sets user type to basic, sets password to "deleted",
    sets username to "[deleted]", sets is_active to FALSE"""
    set_user_group(username, "basic")
    password = generate_password_hash("deleted")
    set_password(username, password)
    sql = "UPDATE users " \
          "SET is_active=FALSE, username='[deleted]' " \
          "WHERE username=:username"
    db.session.execute(sql, {"username": username})
    db.session.commit()


def get_user_id(username):
    """returns -1 if user not found"""
    if not user_exists(username):
        return -1
    sql = "SELECT id " \
          "FROM users " \
          "WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user_id = result.fetchone()[0]
    return user_id


def validate_username(username):
    """returns true if username is 3-20 characters long
    and consists of letters and numbers"""
    if re.match(r"^[a-zA-Z0-9åäöÅÄÖ]{3,20}$", username):
        return True
    return False


def validate_password(password):
    """returns true if password is 10-30 characters long
    and consists of letters and numbers"""
    if re.match(r"^[a-zA-Z0-9]{10,30}$", password):
        return True
    return False
