from flask import flash, session
from os import urandom
from datetime import datetime
import sqlite3
import hashlib
DB_FILE = "data.db"


'''Used to check if user exists with create_user,
reports back int to see if given user has data '''

def count_users(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users WHERE users.username == ?", [username]).fetchall()
    db.close()
    return len(data)

def create_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    ''' Checks if data corresponding to given username is found '''
    if get_user(username):
        flash("User already exists")
        return False
    elif len(username) < 5:
        flash("Username must be at least 5 characters")
        return False
    elif len(password) < 5:
        flash("Password must be at least 5 characters")
        return False
    hash_obj = hashlib.md5(password)
    hashpass = hash_obj.hexdigest()
    ''' If username and password meet length specifications, add name and pass combo to table '''
    c.execute("INSERT INTO users VALUES (?, ?)", [username, hashpass])
    db.commit()
    db.close()
    return True

def login_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = get_user(username)
    ''' Checks if no data can be found on given username '''
    if user == None:
        flash("User does not exist")
        db.close()
        return None
    elif user[1] != password:
        flash("Password is incorrect")
        db.close()
        return None
    ''' Set current session user '''
    session["user"] = username
    db.close()
    return True


def get_user(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = c.execute("SELECT * FROM users WHERE users.username == ?" , [username]).fetchone()
    db.close()
    return user
