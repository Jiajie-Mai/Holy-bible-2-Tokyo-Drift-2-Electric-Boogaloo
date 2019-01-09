import sqlite3
DB_FILE = "app.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()
'''Makes users and posts table'''
c.execute("CREATE TABLE users (id INTEGER, username TEXT, password TEXT)")
c.execute("CREATE TABLE gameData (id INTEGER, money INTEGER, stocksOwned STRING)")

db.commit()
db.close()
