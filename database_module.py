import datetime
import sqlite3
from sqlite3 import Error


dbfile = 'db/money.db'

createsql ='''CREATE TABLE IF NOT EXISTS money(
   date TEXT,
   amount numeric ,
   description TEST
)'''


def createdbIfNotExists():
   print("Checking Table created..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute(createsql)
   conn.commit()
   cursor.close()


def addData(dt, amt, desc):
   print("adding data..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("insert into money (date, amount, description) values (?,?,?)", (dt, amt, desc))
   conn.commit()
   cursor.close()
    

def getBalance():
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("select sum(amount) from money")
   balanceRecord = cursor.fetchone()
   print("balance: ", balanceRecord)
   return balanceRecord[0]
   cursor.close()


def getHistory():
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   cursor = conn.cursor()
   cursor.execute("select * from money ORDER BY date(date) DESC")
   rows = cursor.fetchall();
   cursor.close()
   return rows 



