#!/usr/bin/python

import sys
sys.path.append('/home/pi/RaspberryRelays/script')
import socket
import cgi
import cgitb
import relaylib
cgitb.enable()

form=cgi.FieldStorage()

print "Content-type: text/html\n\n"
if len(form.getvalue('gpioch')) > 0:
   print "Risposta server: ",relaylib.accendi(form.getvalue('host'),int(form.getvalue('port')),int(form.getvalue('gpioch')))
else: 
   print "Nessun argomento per il comando di accensione"

