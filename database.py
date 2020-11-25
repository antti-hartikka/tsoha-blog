from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


def file_input(file):
    name = file.filename
    if not name.endswith(".jpg"):
        return "Invalid filename"
    data = file.read()
    if len(data) > 500 * 1024:
        return "Too big file"
    return data
