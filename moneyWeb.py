from flask import Flask, render_template, request
import datetime
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

dbfile = 'db/money.db'

createsql ='''CREATE TABLE IF NOT EXISTS money(
   date TEXT,
   amount numeric ,
   description TEST
)'''


def addData(dt, amt, desc):
   print("adding data..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute("insert into money (date, amount, description) values (?,?,?)", (dt, amt, desc))
   conn.commit()
   cursor.close()
    


def createdb(): 
   print("Checking Table created..")
   conn = sqlite3.connect(dbfile)
   cursor = conn.cursor()
   cursor.execute(createsql)
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


@app.route('/history')
def list():
   conn = sqlite3.connect(dbfile)
   conn.row_factory = sqlite3.Row
   
   cursor = conn.cursor()
   cursor.execute("select * from money ORDER BY date(date) DESC")
   
   rows = cursor.fetchall(); 
   cursor.close()
   return render_template("history.html",rows = rows)

@app.route('/add')
def add():
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   templateData = {
       'dt':dateString
   }
   return render_template('add.html', **templateData)


@app.route('/addRec', methods = ['POST', 'GET'])
def addRec():
   if request.method == 'POST':
      try:
         dt = request.form['dt']
         amt = request.form['amt']
         desc = request.form['desc']
         
         addData(dt, amt, desc)   
         msg = "successfully added transaction"
      except:
         msg = "error adding transaction"
      
      finally:
         return render_template("result.html",msg = msg)
  

@app.route("/")
def main():
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   bal = getBalance()
   templateData = {
      'title' : 'Pocket Money Tracker',
      'time': dateString,
      'child': 'William',
      'balance': bal
      }
   return render_template('index.html', **templateData)

if __name__ == "__main__":
   createdb()
   #addData("2021-02-05", 3.00, "starting amount")
   #addData("2021-02-13", 10.00, "payment")
   #addData("2021-02-19", 10.00, "payment")

   # run web
   app.run(host='0.0.0.0', port=8080, debug=True)



