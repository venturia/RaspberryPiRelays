#!/usr/bin/python

import sys
sys.path.append('INSTALLATIONDIRECTORY/script')
import socket
import cgi
import cgitb
import relaylib
cgitb.enable()

form=cgi.FieldStorage()

print "Content-type: text/html\n\n"
if len(form.getvalue('gpioch')) > 0:
   statusresponse=relaylib.stato_gpio(form.getvalue('host'),int(form.getvalue('port')),form.getvalue('gpioch'))
   if statusresponse.find("$0$") >= 0:
      print statusresponse[-2]
   else:
      print "-1"
else: 
   print "Nessun argomento per il comando di richiesta stato canale GPIO"

