import sqlite3
DB_FILE = "multi.db"
def reset():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS a;")
    c.execute("CREATE TABLE a (num INTEGER);")
    c.execute("INSERT INTO a VALUES(0);")
    db.commit()
    db.close()

def increment():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM a;")
    a = c.fetchall()[0][0]
    c.execute("UPDATE a SET num = ?;",(a+1,))
    db.commit()
    db.close()

def getval():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("SELECT * FROM a;")
    a = c.fetchall()[0][0]
    db.close()
    return a
    
if __name__ == "__main__":
    reset()
