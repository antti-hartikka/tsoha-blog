from flask import make_response
from app import db


def get_image(image_id):
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id": image_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response


def add_image(file):
    name = file.filename
    if not name.endswith(".jpg") and not name.endswith(".jpeg") and not name.endswith(".png"):
        return "invalid filename"
    data = file.read()
    if len(data) > 500 * 1024:
        return "file too big"
    sql = "INSERT INTO images (name,data) " \
          "VALUES (:name,:data) " \
          "RETURNING id"
    result = db.session.execute(sql, {"name": name, "data": data})
    db.session.commit()
    image_id = result.fetchone()[0]
    return image_id


def file_input(file):
    name = file.filename
    if not name.endswith(".jpg"):
        return "Invalid filename"
    data = file.read()
    if len(data) > 500 * 1024:
        return "Too big file"
    return data
