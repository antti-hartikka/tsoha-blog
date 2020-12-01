from flask import make_response
from app import db


def get_image(image_id):
    """returns response that can be returned straight to requesting object"""
    sql = "SELECT data FROM images WHERE id=:id"
    result = db.session.execute(sql, {"id": image_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response


def add_image(file):
    """Returns image id if success, returns error message string otherwise"""
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
    """returns data if successful, returns error message string otherwise"""
    name = file.filename
    if not name.endswith(".jpg") or not name.endswith(".jpeg"):
        return "Invalid filename"
    data = file.read()
    if len(data) > 500 * 1024:
        return "Too big file"
    return data
