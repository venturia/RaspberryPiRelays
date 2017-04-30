#!/usr/bin/python


import sys
import StringIO

sys.path.append('/home/pi/RaspberryRelays/script')
import socket
import cgi
import cgitb
import relaylib
cgitb.enable()

statusstring = StringIO.StringIO()
form=cgi.FieldStorage()

print "Content-type: text/html\n\n"
reply,statusdict = relaylib.stato(form.getvalue('host'),int(form.getvalue('port')))
for gpioch,name,status,lock in zip(statusdict['gpioch'],statusdict['name'],statusdict['status'],statusdict['locked']):
     disabled=""
     if lock == 1:
        disabled="disabled"
     if status == 1:
        print >>statusstring, "(GPIO %d) %s  <b><font color='red'>ON</font></b>" % (gpioch,name)
     else:
        print >>statusstring, "(GPIO %d) %s  <font color='grey'>OFF</font>" % (gpioch,name)
 
     print >>statusstring, "<button %s onclick='accensione(%d)'>Accendi</button>" % (disabled,gpioch)
     print >>statusstring, "<button %s onclick='spegnimento(%d)'>Spegni</button><br>" % (disabled,gpioch)

if len(statusstring.getvalue())>0:
     print statusstring.getvalue()
else:
     print reply


