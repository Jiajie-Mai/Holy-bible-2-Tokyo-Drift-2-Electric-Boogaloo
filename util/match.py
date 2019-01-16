import sqlite3

from battlestalker import *

DB_FILE = "multi.db"
MAX_ROUNDS = 5
START_DOSH = 1000
STOCK_NUM = 5

def reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS a;")
    c.execute("CREATE TABLE a (matchid INTEGER PRIMARY KEY, u1 INTEGER, u2 INTEGER, dosh1 INTEGER, dosh2 INTEGER, choice1 INTEGER, choice2 INTEGER, round INTEGER);")
    db.commit()
    db.close()

def add_user(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if(c.execute("SELECT count(*) FROM a WHERE a.u2 == ? OR a.u1 == ?;",(uid,uid)).fetchall()[0][0]==0):
        a = c.execute("SELECT * FROM a WHERE a.u2 == 0;").fetchall()
        print(a)
        if len(a)>0: # if other players are waiting for someone to join a match, join their match, else create a row indicating waiting for match.
            c.execute("UPDATE a SET u2 = ? WHERE a.matchid == ?;",(uid,a[0][0]))
        else:
            q=c.execute("SELECT count(*) FROM a;").fetchall()
            print(q)
            c.execute("INSERT INTO a (matchid, u1, u2) VALUES (?, ?, 0);",(q[0][0]+1,uid))
        db.commit()
        db.close()

def rdy_chk(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.u1 == ? OR a.u2 == ?;",(uid,uid)).fetchall();
    db.close()
    return len(b)>0 and b[0][1]>0 and b[0][2]>0

def rm_match(mid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM a WHERE a.matchid == ?;",(mid,))
    db.commit()
    db.close()

def match_info(uid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.u1 == ? OR a.u2 == ?;",(uid,uid)).fetchall();
    db.close()
    return b[0] if len(b)>0 else None;

def init_match(uid):
    i = match_info(uid)
    if i != None and match_info[7] == None:
        c.execute("UPDATE a SET rounds = ?, dosh1 = ?, dosh2 = ?;", (MAX_ROUNDS, START_DOSH, START_DOSH)) # possible giving players starting $ based on total money?
        add_stocks(i[0],n)

def move(uid, mv):
    i = match_info(uid)
    if i != None and -1*NUM_STOCKS <= mv <= 1*NUM_STOCKS: # - short + buy |mv| stockno, 0 do nothing
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        if i[1] == uid and i[5] == None: # check if u u1 or u2 & that u not already moved this round
            c.execute("UPDATE a SET choice1 = ? WHERE a.mid == ?;",(mv,i[0]))
            db.commit()
            db.close()
            if i[6] != None:
                nxt_round(i[0])
        elif i[6] == None:
            c.execute("UPDATE a SET choice2 = ? WHERE a.mid == ?;",(mv,i[0]))
            db.commit()
            db.close()
            if i[5] != None:
                nxt_round(i[0])

def nxt_round(mid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.matchid == ?;",(matchid,)).fetchone();
    if b != None and b[5] != None and b[6] != None:
        if b[5] != 0:
            s1 = inf_stock(mid, b[5])
            d1 = b[3] + b[3]*s1[2]*(1 if b[5]>0 else -1)
            c.execute("UPDATE a SET dosh1 = ? WHERE a.mid == ?;",(d1, mid))
        if b[6] != 0:
            s2 = inf_stock(mid, b[6])
            d2 = b[4] + b[4]*s1[2]*(1 if b[6]>0 else -1)
            c.execute("UPDATE a SET dosh2 = ? WHERE a.mid == ?;",(d2, mid))
        c.execute("UPDATE a SET round = ?, choice1 = ?, choice2 = ?;",(b[7] - 1, None, None))
        db.commit()
        if b[7] == 1:
            nd_match(mid)
    db.close()
    
# matchid, u1, u2, dosh1, dosh2, choice1, choice2, round
if __name__ == "__main__": # unit testing
    reset()
    add_user(766)
    add_user(554)
    add_user(123)
    add_user(66)
    add_user(5)
    print(rdy_chk(5))
    print(rdy_chk(123))
    init_match(123)
