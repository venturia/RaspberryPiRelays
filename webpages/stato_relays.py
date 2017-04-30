#!/usr/bin/python


import sys
sys.path.append('/home/pi/RaspberryRelays/script')
import socket
import cgi
import cgitb
import relaylib
cgitb.enable()

print "Content-type: text/html\n\n"
print relaylib.stato("localhost",5002)

