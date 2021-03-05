import datetime
import sqlite3
from sqlite3 import Error


dbfile = '/config/money.db'
##dbfile = 'money.db'


def createdbIfNotExists():
   print("Checking Table created..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("create table if not exists money(child text, date text, amount numeric, description text)")
   cursor.execute("create table if not exists child(name text)")
   cursor.execute("create table if not exists schedule(child text, amount numeric, description text, frequency text)")
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


def getSchedules(): 
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select rowid, * from schedule ORDER BY rowid DESC")
   rows = cursor.fetchall()
   cursor.close()
   return rows 

def addSchedule(child, amt, desc, frequency):
   print("adding Schedule..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("insert into schedule (child, amount, description, frequency) values (?,?,?,?)", (child, amt, desc, frequency))
   conn.commit()
   cursor.close()

def deleteSchedule(child, rowid):
   print("deleting schedule record..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("delete from schedule where child = ? and rowid = ?", (child, rowid))
   conn.commit()
   cursor.close()

def deleteAmount(child, rowid):
   print("deleting amount record..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("delete from money where child = ? and rowid = ?", (child, rowid))
   conn.commit()
   cursor.close()
   
def getChildren():
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select name as child from child order by child")
   rows = cursor.fetchall()
   cursor.close()
   return rows    

def getBalances():
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select child, sum(amount) AS balance from money group by child order by child")
   rows = cursor.fetchall()
   cursor.close()
   return rows 

def getHistory(child):
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select rowid, * from money where child = ? ORDER BY date(date) DESC", ([child]))
   rows = cursor.fetchall()
   cursor.close()
   return rows 



