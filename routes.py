from app import app
from flask import redirect, render_template, request, session

import database


@app.route("/")
def index():
    posts = database.get_posts("short")
    return render_template("index.html", posts=posts)


@app.route("/stories")
def stories():
    posts = database.get_posts("long")
    return render_template("stories.html", posts=posts)


@app.route("/stories/<int:id>")
def story(id):
    return render_template("story.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/account/<string:username>")
def account(username):
    user_type = database.get_user_type(username)
    return render_template("account.html", username=username, usergroup=user_type)


@app.route("/create_long")
def create_long():
    return render_template("/create_long_post.html")


@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    database.create_user(username, password, "basic")
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    login_ok = database.check_credentials(username, password)
    if login_ok:
        session["username"] = username
        session["user_type"] = database.get_user_type(username)
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_type"]
    return redirect("/")


@app.route("/create_short")
def create_short():
    return render_template("create_short_post.html")


@app.route("/admintools")
def admintools():
    userlist = database.get_user_list()
    return render_template("admintools.html", users=userlist)


@app.route("/private")
def private():
    return render_template("/private.html")


@app.route("/get_user", methods=["POST"])
def get_user():
    user = request.form["username"]
    return redirect("/account/" + user)
