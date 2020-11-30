import accounts
from message import db


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