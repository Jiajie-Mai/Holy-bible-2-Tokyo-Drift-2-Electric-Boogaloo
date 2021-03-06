import sqlite3
import json


from util.battlestalker import *
from util.db_utils import get_username, d_dogbloon


DB_FILE = "multi.db"
MAX_ROUNDS = 5
START_DOSH = 100000
STOCK_NUM = 5
def reset():
    '''clears all data from table'''
    s_reset()
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS a;")
    c.execute("CREATE TABLE a (matchid INTEGER PRIMARY KEY, u1 INTEGER, u2 INTEGER, dosh1 INTEGER, dosh2 INTEGER, choice1 INTEGER, choice2 INTEGER, round INTEGER);")
    db.commit()
    

def add_user(uid):
    '''adds a user to the list looking for matches, either placing them in a match with another user or searching for a match for them by themselves'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if  uid == None or uid == 0:
        return False
    if c.execute("SELECT count(*) FROM a WHERE a.u2 == ? OR a.u1 == ?;",(uid,uid)).fetchall()[0][0]==0:
        a = c.execute("SELECT * FROM a WHERE a.u2 == 0;").fetchall()
        if len(a)>0: # if other players are waiting for someone to join a match, join their match, else create a row indicating waiting for match.
            c.execute("UPDATE a SET u2 = ? WHERE a.matchid == ?;",(uid,a[0][0]))
            db.commit()
            db.close()
            init_match(uid)
        else:
            q=c.execute("SELECT matchid FROM a;").fetchall()
            print(q)
            c.execute("INSERT INTO a (matchid, u1, u2) VALUES (?, ?, 0);",(min_new_id(q),uid))
            db.commit()
            
        return True
        
def min_new_id(q):
    '''returns the lowest id not in q so we don;t have duplicate ids because uhh that would b bad'''
    if len(q) == 0:
        return 1
    i = 1
    b = set(j[0] for j in q)
    while i < 5000: # will crash after 5000 simeltaneous but it's not like we have servers to support a ton of traffic anyways nor do I expect + 10,000 to use this website at once so not really a problem
        if i not in b:
            return i
        i += 1
    return 1

def rdy_chk(uid):
    '''checks a match found by searching for one user to see if to players have been found'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.u1 == ? OR a.u2 == ?;",(uid,uid)).fetchall();
    db.close()
    return len(b)>0 and b[0][1]>0 and b[0][2]>0

def rm_match(mid):
    '''obliterates a match from out of existence pretty epic really'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("DELETE FROM a WHERE a.matchid == ?;",(mid,))
    db.commit()
    

def ok2rm(uid):
    '''marks a user as having left from the match screen. once both users leave, match gets removed.'''
    i = matchinfo(uid)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if i!=None and i[7]==0:
        if i[2] == -1 or i[1] == -1:
            db.close()
            rn_match(i[0])
        elif i[1] == uid:
            c.execute("UPDATE a SET u1 = -1 WHERE a.matchid == ?;",(mid,)) # 0 represents slot open to player joining for match, -1 already ended match.
        else:
            c.execute("UPDATE a SET u2 = -1 WHERE a.matchid == ?;",(mid,))
    db.commit()
    db.close()

def match_info(uid):
    '''returns database row for match with uid as player'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.u1 == ? OR a.u2 == ?;",(uid,uid)).fetchall();
    db.close()
    return b[0] if len(b)>0 else None;

def init_match(uid):
    '''sets up database values for start of match (starting currency, rounds left)'''
    i = match_info(uid)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if i != None and i[7] == None:
        c.execute("UPDATE a SET round = ?, dosh1 = ?, dosh2 = ? WHERE a.matchid == ?;", (MAX_ROUNDS, START_DOSH, START_DOSH, i[0])) # possible giving players starting $ based on total money?
        add_stocks(i[0],STOCK_NUM)
    db.commit()
    db.close()
    
def move(uid, mv):
    '''marks a player as having made a move, if both players have moved advances to next round'''
    i = match_info(uid)
    if i != None and i[7]>0 and -1*STOCK_NUM <= int(mv) <= 1*STOCK_NUM: # - short + buy |mv| stockno, 0 do nothing
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        if i[1] == uid and i[5] == None: # check if u u1 or u2 & that u not already moved this round
            c.execute("UPDATE a SET choice1 = ? WHERE a.matchid == ?;",(int(mv),i[0]))
            db.commit()
            db.close()
            if i[6] != None:
                nxt_round(i[0])
        elif i[2] == uid and i[6] == None:
            c.execute("UPDATE a SET choice2 = ? WHERE a.matchid == ?;",(int(mv),i[0]))
            db.commit()
            db.close()
            if i[5] != None:
                nxt_round(i[0])

def nxt_round(mid):
    '''calculats change in $ based on stocks purchased, decrements rounds left, generates a new list of stocks.'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    b = c.execute("SELECT * FROM a WHERE a.matchid == ?;",(mid,)).fetchone();
    if b != None and b[5] != None and b[6] != None:
        if b[5] != 0:
            s1 = inf_stock(mid, b[5])
            d1 = int(b[3] + b[3]*s1[4]*(1 if b[5]>0 else -1))
            print(d1)
            c.execute("UPDATE a SET dosh1 = ? WHERE a.matchid == ?;",(d1, mid))
        if b[6] != 0:
            s2 = inf_stock(mid, b[6])
            d2 = int(b[4] + b[4]*s2[4]*(1 if b[6]>0 else -1))
            print(d2)
            c.execute("UPDATE a SET dosh2 = ? WHERE a.matchid == ?;",(d2, mid))
        if d2 <= 0 or d1 <= 0:
            b[7] = 1
        c.execute("UPDATE a SET round = ?, choice1 = ?, choice2 = ?;",(b[7] - 1, None, None))
        db.commit()
        db.close()
        if b[7] > 1:
            rm_stocks(mid)
            add_stocks(mid,STOCK_NUM)
        else:
            distr_winnings(mid)
            
def distr_winnings(mid):
    '''after match has ended, picks winners and gives them money'''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()  
    b = c.execute("SELECT * FROM a WHERE a.matchid == ?;",(mid,)).fetchone();
    if b != None and b[7] == 0:
        if b[3] > b[4]:
            d_dogbloon(b[1], START_DOSH / 100)
            d_dogbloon(b[2], START_DOSH / 100 * -1)
        elif b[4] > b[3]:
            d_dogbloon(b[1], START_DOSH / 100 * -1)
            d_dogbloon(b[2], START_DOSH / 100)
    db.commit()
    db.close()

def match_info_json(uid): # returns all relavent info about match as json -- match id, players, money, round, stocks (not price change ofc).
    '''json string of info on match & stocks in display players need to display.'''
    b = match_info(uid)    
    if b != None:
        s = inf_stock(b[0],0)
        if len(s) > 0:
            if uid == b[1]:
                d = {"p":get_username(b[1]), "pdosh":int(b[3]), "e":get_username(b[2]), "edosh":int(b[4]), "round":b[7], "stocks":[(i[2],i[3]) for i in s]}
            else:
                d = {"p":get_username(b[2]), "pdosh":int(b[4]), "e":get_username(b[1]), "edosh":int(b[3]), "round":b[7], "stocks":[(i[2],i[3]) for i in s]}
            return json.dumps(d)

if __name__ == "__main__": # unit testing
    reset()
    s_reset()
    add_user(766)
    add_user(554)
    add_user(123)
    add_user(66)
    add_user(5)
    print(rdy_chk(5))
    print(rdy_chk(123))
    print(match_info_json(123))
