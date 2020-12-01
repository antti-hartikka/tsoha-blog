import accounts
from app import db


def get_comments(post_id):
    """Returns list of tuples where [0]: timestamp, [1]: username
    [2]: comment, [3]: id"""
    sql = "SELECT c.time_created, u.username, c.comment, c.id FROM comments c " \
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


def remove_comment(comment_id):
    sql = "DELETE FROM comments WHERE id=:comment_id"
    db.session.execute(sql, {"comment_id": comment_id})
    db.session.commit()
