import os
from flask import Flask, render_template, request, Response, send_from_directory, Blueprint, flash, g, redirect
from functools import wraps 
from flask import current_app as app
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
import datetime

from pocket import db as db
from .nav import nav

money = Blueprint("money", __name__)


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


nav.register_element('money_top', Navbar( View('Pocket Money Tracker', '.home'), View('Schedules', '.schedules'), View('Add Child', '.addChild')))


@money.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@money.route('/history/<child>')
def history(child):
   rows = db.getHistory(child); 
   return render_template("history.html",rows = rows, child = child)


@money.route('/add/<child>')
@requires_auth
def add(child):
   now = datetime.datetime.now()
   dateString = now.strftime("%d/%m/%Y")
   templateData = {
       'child': child,
       'dt':dateString
   }
   return render_template('add.html', **templateData)

@money.route('/schedules', methods = ['POST', 'GET'])
def schedules():
   rows = db.getSchedules()
   return render_template('schedule.html', rows = rows)


@money.route('/deleteSchedule/<child>/<rowid>')
@requires_auth
def deleteSchedule(child, rowid):
  try:
     print("Deleting schedule record")
     db.deleteSchedule(child, rowid)
     msg = "Successfully deleted record"
  except Exception as e:
     print(e)
     msg = "Error deleting record, please retry"
  finally:
     flash(msg)
     return redirect('/')

@money.route('/deleteAmount/<child>/<rowid>')
@requires_auth
def deleteAmount(child, rowid):
  try:
     print("Deleting record")
     db.deleteAmount(child, rowid)   
     msg = "Successfully deleted record"
  except Exception as e: 
     print(e)
     msg = "Error deleting record, please retry"
  finally:
     flash(msg)
     return redirect('/')


@money.route('/addRec', methods = ['POST', 'GET'])
def addRec():
   if request.method == 'POST':
      try:
         child = request.form['child']
         dt = request.form['dt']
         amt = request.form['amt']
         desc = request.form['desc']
         
         db.addData(child, dt, amt, desc)   
         msg = "Successfully added transaction"
      except:
         msg = "Error adding transaction, please retry"
      
      finally:
         flash(msg)
         return redirect('/')
  
@money.route('/addChildRec', methods = ['POST', 'GET'])
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
         flash(msg)
         return redirect('/')
  

@money.route('/addChild')
def addChild(): 
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   return render_template('addchild.html', title = 'Pocket Money Tracker', time = dateString)


@money.route("/")
def home():
   now = datetime.datetime.now()
   dateString = now.strftime("%Y-%m-%d")
   rows = db.getBalances()

   if len(rows) == 0:
       return render_template('addchild.html', title = 'Pocket Money Tracker', time = dateString)
   else:
       return render_template('index.html', rows = rows, title = 'Pocket Money Tracker', time = dateString)







