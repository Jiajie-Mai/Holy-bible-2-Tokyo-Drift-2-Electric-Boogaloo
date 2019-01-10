from flask import Flask, render_template, request, session, redirect, url_for, flash
from util.db_utils import create_user, login_user
from os import urandom
import hashlib

from test import *

app = Flask(__name__)
app.secret_key = urandom(32)

IEXTRADING_URL-STUB="https://api.iextrading.com/1.0"

@app.route("/index", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    '''Looks for current user; if exists, redirs them to homepage.  Otherwise, sends them to signup page'''
    if "user" in session.keys():
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("signup.html", title = "Sign Up", current_user = session.get("user"))
    else:
        username = request.form.get("username")
        password = request.form.get("password").encode('utf-8')
        '''Hash used to secure password'''
        hash_obj = hashlib.md5(password)
        hashpass = hash_obj.hexdigest()
        if create_user(username, password):
            login_user(username, hashpass)
            return redirect(url_for("/"))
        return render_template("signup.html", title = "Sign Up")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if "user" in session.keys():
        return redirect(url_for("index"))
    if request.method == "GET":
        return render_template("login.html", title = "Login", current_user = session.get("user"))
    else:
        username = request.form.get("username")
        password = request.form.get("password").encode('utf-8')
        '''Hashes password input to see if this hash matches with auth hash'''
        hash_obj = hashlib.md5(password)
        hashpass = hash_obj.hexdigest()
        login = login_user(username, hashpass)
        '''If login fail, redir to login page, otherwise send user to homepage'''
        if login == None:
            return render_template("login.html", title = "Login")
        return redirect(url_for("index"))


@app.route("/logout", methods = ["GET"])
def logout():
    '''Removes current user from session.keys()'''
    if "user" in session.keys():
        session.pop("user")
    return redirect(url_for("login"))


@app.route("/u/<username>", methods = ["GET"])
def profile(username):
    '''Homepage if logged in to specific account'''
    return render_template("profile.html", user = username, posts = get_posts(username)[::-1], current_user = session.get("user"))


@app.route("/create_post", methods = ["POST"])
def create_post():
    insert_post(request.form.get("blog_post"))
    return redirect(request.referrer)


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    if request.method == "GET":
        post = get_post(post_id)
        '''If the user of the post doesn't match current user, redirs them to profile page'''
        if(post[1] != session.get("user")):
            return redirect(url_for("profile", username = post[1]))
        return render_template("profile.html", user = session.get("user"), current_user = session.get("user"), posts = get_posts(get_post(post_id)[1])[::-1], edit_id = post_id)

    post = get_post(post_id)
    if(post[1] != session.get("user")):
        return redirect(url_for("profile", username = post[1]))
    edit_post(post_id, request.form.get("blog_post"))
    return render_template("profile.html", user = post[1], posts = get_posts(get_post(post_id)[1])[::-1], current_user = session.get("user"))

@app.route("/stock")
def stockData():
    return redirect(url_for("stock"))

@app.route("/battle")
def battleData():
    return redirect(url_for("battle"))

@app.route("/userinf")
def userData():
    return redirect(url_for("userinf"))



@app.route("/thing")
def game():
    return render_template("test.html")

@app.route("/inc")
def game1():
    increment()
    return str(getval())

@app.route("/val")
def game2():
    return str(getval())


if __name__ == "__main__":
    app.debug = True
    app.run()
