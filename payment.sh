#!/bin/bash

echo "`date` Starting payment for child: $1 and amount: $2" >> /config/payment.log

export PATH=.:/pocket/:/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

/payment.py $1 $2
