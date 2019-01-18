from os import urandom

from flask import Flask, render_template, request, session, redirect, url_for, flash
import hashlib

from util.db_utils import create_user, login_user, get_user, get_dogbloons, get_userId, change_pass, get_pass
import util.match as match
from util.apiOperator import doggyPicture

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", current_user = session.get("user"))

'''Reroutes users to make an account'''
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    '''Looks for current user; if exists, redirs them to homepage.  Otherwise, sends them to signup page'''
    if "user" in session.keys():
        return redirect(url_for("home"))
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
            return redirect(url_for("home"))
        return render_template("signup.html", title = "Sign Up")

'''Reroutes users to login to their account'''
@app.route("/login", methods = ["GET", "POST"])
def login():
    if "user" in session.keys():
        return redirect(url_for("home"))
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
        return redirect(url_for("home"))

'''Allows users to exit their account and redirects to home page'''
@app.route("/logout", methods = ["GET"])
def logout():
    '''Removes current user from session.keys()'''
    if "user" in session.keys():
        session.pop("user")
    return redirect(url_for("login"))

'''Displays user info'''
@app.route("/u/<username>", methods = ["GET"])
def profile(username):
    '''Homepage if logged in to specific account'''
    try:
        return render_template("userinf.html", user = username, current_user = session.get("user"), money=get_dogbloons(get_userId(session.get("user"))))
    except IndexError:
        return redirect("/")

'''Reroutes user to change current password'''
@app.route("/change_password", methods = ["GET", "POST"])
def change_password():
    if request.method == "GET":
        return render_template("change_password.html", title = "Sign Up", current_user = session.get("user"))
    oldpass = request.form.get("oldpass").encode('utf-8')
    newpass = request.form.get("newpass").encode('utf-8')
    confpass = request.form.get("confpass").encode('utf-8')
    conf = change_pass(oldpass, newpass, confpass, session.get("user"))
    '''If login fail, redir to login page, otherwise send user to homepage'''
    if conf:
        return redirect(url_for("home"))
    return render_template("change_password.html", title = "Change Your Password", current_user =session.get("user"))


@app.route("/stock")
def stockData():
    return redirect(url_for("stock"))

@app.route("/find")
def find():
    try:
        match.add_user(get_userId(session.get("user")))
        return render_template("find.html")
    except IndexError:
        return redirect("/")

'''Allows users to find other users to battle'''
@app.route("/findv")
def findv():
    try:
        return "true" if match.rdy_chk(get_userId(session.get("user"))) else "false"
    except IndexError:
        return "false"

'''Reroutes to battle system'''
@app.route("/battle")
def battle():
    if session.get("user") == None:
        return redirect("/")
    return render_template("battle.html", doggo1 = doggyPicture(), doggo2 = doggyPicture())

@app.route("/minf")
def minf():
    try:
        return str(match.match_info_json(get_userId(session.get("user"))))
    except IndexError:
        return "None"

@app.route("/mv", methods=["GET"])
def mv():
    mv = request.args.get("dir")
    try:
        match.move(get_userId(session.get("user")), mv if mv != None else 0)
        return ","
    except IndexError:
        return "?"


'''Win conditions'''
@app.route("/win")
def v():
    flash("You dogged persistence carried you to victory.")
    return redirect("/")
@app.route("/loss")
def l():
    flash("Sadly, a defeat. Maybe not every dog has their day.")
    return redirect("/")
@app.route("/tie")
def t():
    flash("A tie! And it was so doggone close!")
    return redirect("/")
if __name__ == "__main__":
    match.reset()

    app.debug = True
    app.run()
