from os import urandom

from flask import Flask, render_template, request, session, redirect, url_for, flash
import hashlib

from util.db_utils import create_user, login_user, get_user, get_dogbloons, get_userId, change_pass, get_pass
import util.match as match
app = Flask(__name__)
app.secret_key = urandom(32)

#API for IEX Trading
#you need to get the stock and place it btwn stub and ender
IEXTRADING_TEST = "https://api.iextrading.com/1.0/stock/aapl/batch?types=quote,news,chart&range=1m&last=10"
IEX_STUB = "https://api.iextrading.com/1.0/"
IEX_ENDER = "batch?types=quote,news,chart&range=1m&last=10"

#API for Random Dog Images
DOG_STUB = "https://dog.ceo/api/breeds/image/random"

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", current_user = session.get("user"))

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


@app.route("/logout", methods = ["GET"])
def logout():
    '''Removes current user from session.keys()'''
    if "user" in session.keys():
        session.pop("user")
    return redirect(url_for("login"))


@app.route("/u/<username>", methods = ["GET"])
def profile(username):
    '''Homepage if logged in to specific account'''
    return render_template("userinf.html", user = username, current_user = session.get("user"), money=get_dogbloons(get_userId(session.get("user"))))

@app.route("/change_password", methods = ["GET", "POST"])
def change_password():
    oldpass = request.form.get("oldpass")
    newpass = request.form.get("newpass")
    confpass = request.form.get("confpass")
    conf = change_pass(oldpass, newpass, confpass, session.get("user"))
    '''If login fail, redir to login page, otherwise send user to homepage'''
    if conf == None:
        return render_template("change_password.html", title = "Change Your Password" )
    return redirect(url_for("home"))

@app.route("/stock")
def stockData():
    return redirect(url_for("stock"))

@app.route("/find")
def find():
    try:
        match.add_user(get_userId(session.get("user")))
        return render_template("find.html")
    except IndexError:
        flash("not logged in")
        return redirect("/")

@app.route("/findv")
def findv():
    try:
        return "true" if match.rdy_chk(get_userId(session.get("user"))) else "false"
    except IndexError:
        return "false"

@app.route("/battle")
def battle():
    return render_template("battle.html")

#@app.route("/thing")
#def game():
#    return render_template("test.html")
#
#@app.route("/inc")
#def game1():
#    increment()
#    return str(getval())
#
#@app.route("/val")
#def game2():
#    return str(getval())

if __name__ == "__main__":
    match.reset()
    app.debug = True
    app.run()
