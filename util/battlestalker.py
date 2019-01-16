import sqlite3
DB_FILE = "battlestalks.db"
def reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS s;")
    c.execute("CREATE TABLE s (matchid INTEGER, symbol TEXT, price INTEGER);")
    db.commit()
    db.close()

def add_match(mid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor
    c.execute()
    db.commit()
    db.close()
