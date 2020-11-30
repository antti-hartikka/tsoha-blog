from flask import Flask

from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
blog_name = getenv("BLOG_NAME")
app.secret_key = getenv("SECRET_KEY")
