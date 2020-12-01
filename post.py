import accounts
from app import db


def create_new_post(username, title, post_type):
    user_id = accounts.get_user_id(username)
    sql = "INSERT INTO posts (user_id, post_type, title, time_created, is_visible)" \
          "VALUES (:user_id, :type, :title, NOW(), TRUE) " \
          "RETURNING id"
    result = db.session.execute(sql, {"user_id": user_id, "type": post_type, "title": title})
    db.session.commit()
    post_id = result.fetchone()[0]
    return post_id


def get_posts(post_type):
    sql = "SELECT * " \
          "FROM posts " \
          "WHERE post_type=:post_type AND is_visible = TRUE " \
          "ORDER BY time_created DESC"
    result = db.session.execute(sql, {"post_type": post_type})
    post_list = result.fetchall()
    return post_list


def get_post(post_id):
    sql = "SELECT p.title, p.time_created, u.username " \
          "FROM posts p " \
          "JOIN users u on u.id = p.user_id " \
          "WHERE is_visible = TRUE AND p.id=:id"
    result = db.session.execute(sql, {"id": post_id})
    post = result.fetchone()
    return post


def remove_post(post_id):
    sql = "UPDATE posts SET is_visible = FALSE WHERE id=:post_id"
    db.session.execute(sql, {"post_id": post_id})
    db.session.commit()
