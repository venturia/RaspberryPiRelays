#!/usr/bin/python

import sys
sys.path.append('/home/pi/RaspberryRelays/script')
import socket
import cgi
import cgitb
import relaylib
cgitb.enable()

print "Content-type: text/html\n\n"
if len(sys.argv) > 1:
   print "Risposta server: ",relaylib.spegni("localhost",5002,int(sys.argv[1]))
else: 
   print "Nessun argomento per il comando di spegnimento"

