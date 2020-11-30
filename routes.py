from app import app
from flask import redirect, render_template, request, session

import database
import accounts
import content
import os


@app.route("/")
def index():
    posts = content.get_shorts("short")
    print(posts)
    contents = [[], [], []]
    count = 0;
    for i in range(3):
        for j in range(3):
            print(count)
            print(len(posts))
            if count == len(posts):
                print(contents)
                return render_template("index.html", posts=contents)
            else:
                contents[i].append(posts[count])
                count += 1

    return render_template("index.html", posts=contents)


@app.route("/stories")
def stories():
    posts = content.get_posts("long")
    return render_template("stories.html", stories=posts)


@app.route("/story/<int:story_id>", methods=["GET", "POST"])
def story(story_id):
    if request.method == "GET":
        post = content.get_post(story_id)
        postcontent = content.get_content(story_id)
        comments = database.get_comments(story_id)
        return render_template("story.html", post=post, contents=postcontent, comments=comments)
    else:
        if len(session) != 0:
            if session["csrf_token"] != request.form["csrf_token"]:
                return redirect("/logout")
            username = session["username"]
            comment = request.form["comment"]
            database.insert_comment(username, story_id, comment)
        return redirect(f"/story/{story_id}")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        result = accounts.create_user(username, password)
        if result == "ok":
            session["username"] = username
            session["user_type"] = accounts.get_usergroup(username)
            session["csrf_token"] = os.urandom(16).hex()
            return redirect("/")
        else:
            return render_template("signup.html", error=result)


@app.route("/account")
def account_noname():
    if session["username"] is None:
        redirect("/")
    return redirect("/account/" + session["username"])


@app.route("/account/<string:username>", methods=["GET", "POST"])
def account(username):
    user_type = accounts.get_usergroup(username)
    if request.method == "GET":
        return render_template("account.html", username=username, usergroup=user_type)
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            return redirect("/logout")

        action = request.form["action"]
        result = "ok"
        if action == "update username":
            new_username = request.form["new_username"]
            result = accounts.set_username(username, new_username)
            if result == "ok":
                session["username"] = new_username
                return redirect("/account")
        if action == "update password":
            old_password = request.form["old_password"]
            if accounts.check_credentials(username, old_password):
                new_password = request.form["new_password"]
                result = accounts.set_password(username, new_password)
            else:
                result = "wrong password"
        if action == "update usergroup":
            new_usergroup = request.form["new_usergroup"]
            accounts.set_usergroup(username, new_usergroup)
            user_type = new_usergroup
        if action == "remove account":
            accounts.delete_account(username)
            return render_template("index.html", msg="tietosi on onnistuneesti poistettu")
        return render_template("account.html", msg=result, username=username, usergroup=user_type)


@app.route("/create_long", methods=["GET", "POST"])
def create_long():
    if request.method == "GET":
        return render_template("create_long_post.html")
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            return redirect("/logout")

        username = session["username"]
        title = request.form["title"]
        post_type = "long"
        post_id = content.create_new_post(username, title, post_type)
        print(request.form)

        form_count = int(request.form["count"])
        for i in range(form_count):
            action = request.form[f"{i}action"]
            if action == "paragraph":
                value = request.form[f"{i}"]
                content_type = "text"
                content.add_content(post_id, None, content_type, value)
            else:
                file = request.files[f"{i}"]
                alternative = request.form[f"{i}a"]
                image_id = content.add_image(file)
                content_type = "image"

                # if file input returns error string
                if type(image_id) is str:
                    return render_template("create_long_post.html", msg=image_id)
                else:
                    content.add_content(post_id, image_id, content_type, alternative)

        return redirect("/stories")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    login_ok = accounts.check_credentials(username, password)
    if login_ok:
        session["username"] = username
        session["user_type"] = accounts.get_usergroup(username)
        session["csrf_token"] = os.urandom(16).hex()
        return redirect("/")
    else:
        return render_template("index.html", login="error")


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_type"]
    del session["csrf_token"]
    return redirect("/")


@app.route("/create_short", methods=["GET", "POST"])
def create_short():
    if request.method == "GET":
        return render_template("create_short_post.html")
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            return redirect("/logout")
        username = session["username"]
        post_type = request.form["type"]

        file = request.files["file"]
        image_id = content.add_image(file)
        if type(image_id) is str:
            return render_template("create_short_post.html", msg=image_id)

        content_type = "image"
        text = request.form["alternative"]

        post_id = content.create_new_post(username, None, post_type)
        content.add_content(post_id, image_id, content_type, text)

        return redirect("/")


@app.route("/admintools", methods=["GET", "POST"])
def admintools():
    if request.method == "GET":
        if session["user_type"] != "admin":
            redirect("/")
        user_list = accounts.get_user_list()
        return render_template("admintools.html", users=user_list)
    else:
        user = request.form["username"]
        return redirect("/account/" + user)


@app.route("/private")
def private():
    return render_template("private.html")


@app.route("/show/<int:image_id>")
def show(image_id):
    return content.get_image(image_id)


@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "GET":
        return render_template("message.html")
    else:
        username = "guest"
        if len(session) != 0:
            if session["csrf_token"] != request.form["csrf_token"]:
                return redirect("/logout")
            username = session["username"]

        user_message = request.form["message"]
        if len(user_message) > 2000:
            return render_template("message.html", msg="liian pitkä viesti :(")

        database.insert_message(username, user_message)

        return render_template("message.html", msg="viestin lähetys onnistui")


@app.route("/show_messages", methods=["GET", "POST"])
def show_messages():
    if session["user_type"] != "admin":
        return redirect("/")
    if request.method == "GET":
        message_list = database.get_messages()
        return render_template("show_messages.html", messages=message_list)
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            return redirect("/logout")

        message_id = request.form["message_id"]
        database.delete_message(message_id)
        return redirect("/show_messages")
