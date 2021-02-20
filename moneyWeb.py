import os
from flask import Flask, render_template, request, Response, send_from_directory
from functools import wraps 
import datetime

import database_module as db

app = Flask(__name__)



def check_auth(username, password):
    return username == 'admin' and password == '0000'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/history')
def list():
   rows = db.getHistory(); 
   return render_template("history.html",rows = rows)


@app.route('/add')
@requires_auth
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
         
         db.addData(dt, amt, desc)   
         msg = "successfully added transaction"
      except:
         msg = "error adding transaction"
      
      finally:
         return render_template("result.html",msg = msg)
  

@app.route("/")
def index():
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   bal = db.getBalance()
   templateData = {
      'title' : 'Pocket Money Tracker',
      'time': dateString,
      'child': 'William',
      'balance': "{:,.2f}".format(bal)
      }
   return render_template('index.html', **templateData)



def main():
   # create db if not exists
   db.createdbIfNotExists()
   app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
   main()




