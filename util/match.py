import sqlite3
DB_FILE = "multi.db"

def reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS a;")
    c.execute("CREATE TABLE a (matchid INTEGER PRIMARY KEY, u1 INTEGER, u2 INTEGER);")
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
            c.execute("INSERT INTO a VALUES (?, ?, 0);",(q[0][0]+1,uid))
        db.commit()
        db.close()
def rdy_chk(uid):
    print(uid)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.u1 == ? OR a.u2 == ?;",(uid,uid)).fetchall();
    print(b)
    db.close()
    return len(b)>0 and b[0][1]>0 and b[0][2]>0

def nd_match(mid):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM a WHERE a.matchid == ?;",(mid,))
    db.commit()
    db.close()
    
if __name__ == "__main__":
    reset()
    add_user(766)
    add_user(554)
    add_user(123)
    add_user(66)
    add_user(5)
    print(rdy_chk(5))
    print(rdy_chk(123))
    nd_match(1)
    nd_match(404)
