import sqlite3
import hashlib

DB_FILE = "app.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

defPass="hello".encode('utf-8')
hash_obj= hashlib.md5(defPass)
hashpass=hash_obj.hexdigest()

'''Default users'''
c.execute("INSERT INTO users VALUES(?, ?, ?);", (123, 'raday', hashpass))
c.execute("INSERT INTO users VALUES(?, ?, ?);", (456, 'jmai', hashpass))
c.execute("INSERT INTO users VALUES(?, ?, ?);", (789, 'tpeters', hashpass))

c.execute("INSERT INTO gameData VALUES(?, ?, ?);", (123, 1000, "AAPL"))
c.execute("INSERT INTO gameData VALUES(?, ?, ?);", (456, 2000, "GOOG"))
c.execute("INSERT INTO gameData VALUES(?, ?, ?);", (789, 42069, "AMZN"))

#VERY IMPORTANT-- HASHED PASSWORDS are 'hello', not the ones you had yesterday

db.commit()
db.close()
