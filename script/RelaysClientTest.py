#!/usr/bin/python

import sys
import socket
import cgi
import cgitb
cgitb.enable()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5002))
if len(sys.argv) > 1:
   client_socket.send(sys.argv[1])

print "Content-type: text/html\n\n"
print sys.argv[1]," eseguito"
client_socket.close()

