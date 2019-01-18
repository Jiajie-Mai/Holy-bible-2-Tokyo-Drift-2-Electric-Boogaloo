import sqlite3

from util.apiOperator import *

DB_FILE = "battlestalks.db"


def s_reset():
    '''clears all data from stocks database'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS s;")
    c.execute("CREATE TABLE s (stockno INTEGER, matchid INTEGER, symbol TEXT, name TEXT, change INTEGER);")
    db.commit()
    db.close()

def add_stocks(mid, n):
    '''generates a random list of n stocks and ads to database under matchid & each with different stockno'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    stocks = randSymbols(n)
    for (i,s) in enumerate(stocks, start=1): # i know, it's awful, but 0 == -0 so i have no choice :(
        c.execute("INSERT INTO s VALUES(?, ?, ?, ?, ?);", (i, mid, *s))
    db.commit()
    db.close()

def inf_stock(mid, stockno):
    '''info on a spacific stock used in a match by stockno, or all the stocks if stockno == 0'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if stockno == 0:
        b=c.execute("SELECT * FROM s WHERE s.matchid==?;", (mid,)).fetchall()
    else:
        b=c.execute("SELECT * FROM s WHERE s.matchid==? AND s.stockno==?;",(mid,abs(stockno))).fetchone()
    db.close()
    return b

def rm_stocks(mid):
    '''deletes the stocks for a certain match '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM s WHERE s.matchid == ?;",(mid,))
    db.commit()
    db.close()
    
if __name__ == "__main__":
    reset()
    add_stocks(3)
