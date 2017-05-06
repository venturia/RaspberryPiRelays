#!/usr/bin/python


import sys
import StringIO

sys.path.append('INSTALLATIONDIRECTORY/script')
import socket
import cgi
import cgitb
import relaylib
cgitb.enable()

statusstring = StringIO.StringIO()
form=cgi.FieldStorage()

print "Content-type: text/html\n\n"
reply,statusdict = relaylib.stato(form.getvalue('host'),int(form.getvalue('port')))
for gpioch,name,status,lock,nbits,bitstatus in zip(statusdict['gpioch'],statusdict['name'],statusdict['status'],statusdict['locked'],statusdict['nbits'],statusdict['bitstatus']):
     disabled=""
     if lock == 1:
        disabled="disabled"
     if status == 1:
        print >>statusstring, "(GPIO %d) %s  <b><font color='red'>ON</font></b>" % (gpioch,name)
     else:
        print >>statusstring, "(GPIO %d) %s  <font color='grey'>OFF</font>" % (gpioch,name)
 
     print >>statusstring, "<button %s onclick='accensione(%d)'>Accendi</button>" % (disabled,gpioch)
     print >>statusstring, "<button %s onclick='spegnimento(%d)'>Spegni</button>" % (disabled,gpioch)
     if nbits > 1:
        for i in range(nbits):
           checked=""
           if bitstatus & 2**i == 2**i:
              checked="checked"
           print >>statusstring, "<input type='checkbox' id='%d_%d' value=%d %s %s> %d " % (gpioch,i,2**i,checked,disabled,i)
        print >>statusstring, "<button %s onclick='configurazione_bitmask(%d,%d)'>Configura</button>" % (disabled,gpioch,nbits)
     print >>statusstring, "<br>"

if len(statusstring.getvalue())>0:
     print statusstring.getvalue()
else:
     print reply


