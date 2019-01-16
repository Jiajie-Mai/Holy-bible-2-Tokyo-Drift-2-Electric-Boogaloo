import sqlite3

from apiOperator import *

DB_FILE = "battlestalks.db"
STOCK_NUM = 5


def reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS s;")
    c.execute("CREATE TABLE s (matchid INTEGER, symbol TEXT, name TEXT, change INTEGER);")
    db.commit()
    db.close()

def add_stocks(mid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    stocks = randSymbols(STOCK_NUM)
    for i in stocks:
        print((mid, *i))
        c.execute("INSERT INTO s VALUES(?, ?, ?, ?);", (mid, *i))
    db.commit()
    db.close()

def rm_stocks(mid):
    c.execute("DELETE FROM s WHERE s.matchid == ?;",(mid,))

if __name__ == "__main__":
    reset()
    add_stocks(3)
