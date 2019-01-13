import sqlite3
DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()
'''Makes users and posts table'''
c.execute("CREATE TABLE users (username TEXT, password TEXT, id INTEGER)")
c.execute("CREATE TABLE gameData (id INTEGER, money INTEGER, stocksOwned STRING)")

db.commit()
db.close()
