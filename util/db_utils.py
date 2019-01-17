from flask import flash, session
from os import urandom
from datetime import datetime
from random import randint
import sqlite3
import hashlib
DB_FILE = "data.db"


'''Used to check if user exists with create_user,
reports back int to see if given user has data '''

def count_users(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    data = c.execute("SELECT * FROM users WHERE users.username == ?;", (username,)).fetchall()
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
    id_generator = c.execute("SELECT count(*) FROM users;").fetchall()[0][0] + 1
    ''' If username and password meet length specifications, add name and pass combo to table '''
    c.execute("INSERT INTO users VALUES (?, ?, ?);", (username, hashpass, id_generator))
    c.execute("INSERT INTO gameData VALUES (?, ?, ?);", (id_generator, 10000, ""))
    db.commit()
    db.close()
    return True

def login_user(username, password):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = get_user(username)
    print(user)
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

def change_pass(oldpass, newpass, confpass, username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = get_user(username)
    if oldpass != get_pass(user):
        flash("Old password isn't correct")
        db.close()
        return None
    elif len(newpass) < 5:
        flash("New password must be at least 5 characters")
        db.close()
        return None
    elif newpass == confpass:
        flash("Confirmation fail")
        db.close()
        return None
    ''' Set current session user '''
    c.execute("SELECT REPLACE (get_pass(user), get_pass(user), newpass);")
    db.commit()
    db.close()
    return True

def get_user(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = c.execute("SELECT * FROM users WHERE users.username == ?;" , (username,)).fetchone()
    db.close()
    print(user)
    return user

def get_pass(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = get_user(username)
    userId = c.execute("SELECT password FROM users WHERE users.username == ?;" , (username,)).fetchall()
    db.close()
    return userId[0][0]

def get_userId(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    user = get_user(username)
    userId = c.execute("SELECT id FROM users WHERE users.username == ?;" , (username,)).fetchall()
    db.close()
    return userId[0][0]

def get_dogbloons(userId):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    dogbloons = c.execute("SELECT money FROM gameData WHERE gameData.id == ?;" , (userId,)).fetchall()
    db.close()
    return dogbloons[0][0]

def d_dogbloon(userId, d):
    cur = get_dogbloons(userId)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("UPDATE gameData SET money = ? WHERE gameData.id == ?;",(cur + d,userId))
    db.commit()
    db.close()

def get_username(userId):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    u = c.execute("SELECT username FROM users WHERE users.id == ?;", (userId,)).fetchone()
    db.close()
    return None if u == None else u[0]
