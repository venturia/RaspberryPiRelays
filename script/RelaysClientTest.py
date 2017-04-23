#!/usr/bin/python

import sys
import socket
import cgi
import cgitb
import getopt
cgitb.enable()

port=5002
host='localhost'

try:
   opts,args = getopt.getopt(sys.argv[1:],"r:p:")
except getopt.GetoptError:
   print 'RelaysClientTest -r <remote host> -p <port number>'
   sys.exit(2)
for opt,arg in opts:
   if opt == '-p':
      port = int(arg)
   if opt == '-r':
      host = arg

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
if len(args) > 0:
   client_socket.send(args[0])
   reply=[]
   replychunk = client_socket.recv(16)
   while len(replychunk):
     reply.append(replychunk)
     replychunk = client_socket.recv(16)
   print "Content-type: text/html\n\n"
   print "Risposta server: \n",''.join(reply)
client_socket.close()

