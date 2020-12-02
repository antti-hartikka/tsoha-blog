import comment
import image
import post
from app import app
from flask import redirect, render_template, request, session

import messages
import accounts
import content
import os


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        posts = content.get_shorts("short")
        contents = [[], [], []]
        count = 0
        for i in range(5):
            for j in range(3):
                if count == len(posts):
                    return render_template("index.html", posts=contents)
                else:
                    contents[i].append(posts[count])
                    count += 1
        return render_template("index.html", posts=contents)
    else:
        if session["csrf_token"] != request.form["csrf_token"] or session["user_group"] != "admin":
            return redirect("/logout")
        post_id = request.form["post_id"]
        post.remove_post(post_id)
        return redirect("/")


@app.route("/stories", methods=["GET", "POST"])
def stories():
    if request.method == "GET":
        posts = post.get_posts("long")
        return render_template("stories.html", stories=posts)
    else:
        if session["csrf_token"] != request.form["csrf_token"] or session["user_group"] != "admin":
            return redirect("/logout")
        story_id = request.form["story_id"]
        post.remove_post(story_id)
        return redirect("/stories")


@app.route("/story/<int:story_id>", methods=["GET", "POST"])
def story(story_id):
    if request.method == "GET":
        this_story = post.get_post(story_id)
        postcontent = content.get_content(story_id)
        comments = comment.get_comments(story_id)
        return render_template(
            "story.html",
            post=this_story,
            contents=postcontent,
            comments=comments,
            story_id=story_id
        )
    else:
        if len(session) != 0:
            if session["csrf_token"] != request.form["csrf_token"]:
                return redirect("/logout")
            if session["user_group"] == "admin":
                comment_id = request.form["comment_id"]
                comment.remove_comment(comment_id)
            else:
                username = session["username"]
                user_comment = request.form["comment"]
                comment.insert_comment(username, story_id, user_comment)
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
            session["user_group"] = accounts.get_user_group(username)
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
    user_group = accounts.get_user_group(username)
    if request.method == "GET":
        return render_template("account.html", username=username, user_group=user_group)
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
        if action == "update user_group":
            new_user_group = request.form["new_user_group"]
            accounts.set_user_group(username, new_user_group)
            user_group = new_user_group
        if action == "remove account":
            accounts.delete_account(username)
            return render_template("index.html", msg="tietosi on onnistuneesti poistettu")
        return render_template("account.html", msg=result, username=username, user_group=user_group)


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
        post_id = post.create_new_post(username, title, post_type)

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
                image_id = image.add_image(file)
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
        session["user_group"] = accounts.get_user_group(username)
        session["csrf_token"] = os.urandom(16).hex()
        return redirect("/")
    else:
        return render_template("index.html", login="error")


@app.route("/logout")
def logout():
    del session["username"]
    del session["user_group"]
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
        image_id = image.add_image(file)
        if type(image_id) is str:
            return render_template("create_short_post.html", msg=image_id)

        content_type = "image"
        text = request.form["alternative"]

        post_id = post.create_new_post(username, None, post_type)
        content.add_content(post_id, image_id, content_type, text)

        return redirect("/")


@app.route("/admintools", methods=["GET", "POST"])
def admintools():
    if request.method == "GET":
        if session["user_group"] != "admin":
            redirect("/")
        user_list = accounts.get_user_list()
        return render_template("admintools.html", users=user_list)
    else:
        user = request.form["username"]
        return redirect("/account/" + user)


@app.route("/private", methods=["GET", "POST"])
def private():
    if request.method == "GET":
        posts = content.get_shorts("private")
        contents = [[], [], []]
        count = 0
        for i in range(5):
            for j in range(3):
                if count == len(posts):
                    return render_template("private.html", posts=contents)
                else:
                    contents[i].append(posts[count])
                    count += 1
        return render_template("private.html", posts=contents)
    else:
        if session["csrf_token"] != request.form["csrf_token"] or session["user_group"] != "admin":
            return redirect("/logout")
        post_id = request.form["post_id"]
        post.remove_post(post_id)
        return redirect("/")


@app.route("/show/<int:image_id>")
def show(image_id):
    return image.get_image(image_id)


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

        messages.insert_message(username, user_message)

        return render_template("message.html", msg="viestin lähetys onnistui")


@app.route("/show_messages", methods=["GET", "POST"])
def show_messages():
    if session["user_group"] != "admin":
        return redirect("/")
    if request.method == "GET":
        message_list = messages.get_messages()
        return render_template("show_messages.html", messages=message_list)
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            return redirect("/logout")

        message_id = request.form["message_id"]
        messages.delete_message(message_id)
        return redirect("/show_messages")
