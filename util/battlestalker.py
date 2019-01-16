import sqlite3
DB_FILE = "battlestalks.db"
def reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS s;")
    c.execute("CREATE TABLE s (matchid INTEGER, symbol TEXT);")
    db.commit()
    db.close()

def add_match(mid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor
    stocks = ["A", "AA", "AAC", "AAN", "AAP"]
    for i in stocks:
        c.execute("")
    db.commit()
    db.close()
