import sqlite3
import hashlib

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

defPass="hello".encode('utf-8')
hash_obj= hashlib.md5(defPass)
hashpass=hash_obj.hexdigest()

'''Default users'''
c.execute("INSERT INTO users VALUES(?, ?, ?);", ('raday', hashpass, 123456))
c.execute("INSERT INTO users VALUES(?, ?, ?);", ('jmai', hashpass, 456789))
c.execute("INSERT INTO users VALUES(?, ?, ?);", ('tpeters', hashpass, 789012))

c.execute("INSERT INTO gameData VALUES(?, ?, ?);", (123456, 1000, "AAPL"))
c.execute("INSERT INTO gameData VALUES(?, ?, ?);", (456789, 2000, "GOOG"))
c.execute("INSERT INTO gameData VALUES(?, ?, ?);", (789012, 42069, "AMZN"))

#VERY IMPORTANT-- HASHED PASSWORDS are 'hello', not the ones you had yesterday

db.commit()
db.close()
