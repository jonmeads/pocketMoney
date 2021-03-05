#!/usr/bin/env python3

import sys
from pocket import db as db
import datetime

try:
    child = sys.argv[1]
    amt = sys.argv[2]

    now = datetime.datetime.now()
    dt = now.strftime("%Y-%m-%d")

    with open("/config/payment.log", "a") as myfile:
        myfile.write(dt + " Processing payment for child: " + child + ", amount: " + amt)


    db.addData(child, dt, amt, "Payment")

except Exception as e:
    with open("/config/payment.log", "a") as myfile:
        myfile.write(dt + "Error adding payment" + e) 
    
      
finally:
    with open("/config/payment.log", "a") as myfile:
        myfile.write(dt + "Payment completed successfully") 

