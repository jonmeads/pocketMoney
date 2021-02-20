import datetime
import sqlite3
from sqlite3 import Error


dbfile = 'db/money.db'


def createdbIfNotExists():
   print("Checking Table created..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("create table if not exists money(child text, date text, amount numeric, description text)")
   cursor.execute("create table if not exists child(name text)")
   cursor.execute("create table if not exists schedule(child text, amount numeric, frequency text, day text)")
   conn.commit()
   cursor.close()


def addData(child, dt, amt, desc):
   print("adding data..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("insert into money (child, date, amount, description) values (?, ?,?,?)", (child, dt, amt, desc))
   conn.commit()
   cursor.close()
    
def addChild(child, amt, dt):
   print("adding child..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("insert into child (name) values (?)", ([child]));
   conn.commit()
   cursor.close()
   addData(child, dt, amt, "Seeding Amount")


def getBalances():
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select child, sum(amount) AS balance from money group by child order by child")
   rows = cursor.fetchall();
   cursor.close()
   return rows 

def getHistory(child):
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select * from money where child = ? ORDER BY date(date) DESC", ([child]))
   rows = cursor.fetchall();
   cursor.close()
   return rows 



