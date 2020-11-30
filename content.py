from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


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


# returns list of tuples containing content
def get_content(post_id):
    sql = "SELECT user_id, image_id, media_type, media_text " \
          "FROM content c " \
          "JOIN postcontent pc on c.id = pc.content_id " \
          "JOIN posts p on pc.post_id = p.id " \
          "WHERE p.id=:post_id " \
          "ORDER BY c.order_number ASC"
    result = db.session.execute(sql, {"post_id": post_id})
    content = result.fetchall()
    return content


def get_shorts(post_type):
    sql = "SELECT i.id, c.media_text FROM posts p " \
          "JOIN postcontent pc on p.id = pc.post_id " \
          "JOIN content c on pc.content_id = c.id " \
          "JOIN images i on c.image_id = i.id " \
          "WHERE p.post_type = :post_type"
    result = db.session.execute(sql, {"post_type": post_type})
    posts = result.fetchall()
    return posts
