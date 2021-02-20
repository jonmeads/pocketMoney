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

@app.route('/history/<child>')
def history(child):
   rows = db.getHistory(child); 
   return render_template("history.html",rows = rows)


@app.route('/add/<child>')
@requires_auth
def add(child):
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   templateData = {
       'child': child,
       'dt':dateString
   }
   return render_template('add.html', **templateData)

@app.route('/deleteAmount/<child>/<rowid>')
@requires_auth
def deleteAmount(child, rowid):
  try:
     print("Deleting record")
     db.deleteAmount(child, rowid)   
     msg = "successfully deleted record"
  except Exception as e: 
     print(e)
     msg = "error deleting record"
  finally:
     return render_template("result.html",msg = msg)
  



@app.route('/addRec', methods = ['POST', 'GET'])
def addRec():
   if request.method == 'POST':
      try:
         child = request.form['child']
         dt = request.form['dt']
         amt = request.form['amt']
         desc = request.form['desc']
         
         db.addData(child, dt, amt, desc)   
         msg = "successfully added transaction"
      except:
         msg = "error adding transaction"
      
      finally:
         return render_template("result.html",msg = msg)
  
@app.route('/addChildRec', methods = ['POST', 'GET'])
def addChildRec():
   if request.method == 'POST':
      try:
         child = request.form['child']
         amt = request.form['amt']

         if amt is None:
             amt = 0

         now = datetime.datetime.now()
         dt = now.strftime("%Y-%m-%d")

         db.addChild(child, amt, dt)   
         msg = "successfully added child"
      except Exception as e: 
         print(e)
         msg = "error adding child"
      
      finally:
         return render_template("result.html",msg = msg)
  

@app.route('/addChild')
def addChild(): 
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   return render_template('addchild.html', title = 'Pocket Money Tracker', time = dateString)


@app.route("/")
def index():
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   rows = db.getBalances()

   if len(rows) == 0:
       return render_template('addchild.html', title = 'Pocket Money Tracker', time = dateString)
   else:
       return render_template('index.html', rows = rows, title = 'Pocket Money Tracker', time = dateString)



def main():
   # create db if not exists
   db.createdbIfNotExists()
   app.run(host='0.0.0.0', port=8080, debug=True)


if __name__ == "__main__":
   main()




