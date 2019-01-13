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
   print "Risposta server: ",relaylib.configura_bit(form.getvalue('host'),int(form.getvalue('port')),form.getvalue('gpioch'),int(form.getvalue('bitmask')))
else: 
   print "Nessun argomento per il comando di configurazione bit mask"

