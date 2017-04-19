#!/usr/bin/python

import sys
import socket
import getopt
import RPi.GPIO as GPIO

def accensione_relay(gpioch):
    print "Accendo GPIO ",gpioch
    GPIO.output(gpioch,True)    

def spegnimento_relay(gpioch):
    print "Spengo GPIO ",gpioch
    GPIO.output(gpioch,False)    

def stato_relays():
    print "Stampo stato"
    for gpio,name,start,lock in gpioattrs:
       print gpio,name,lock,GPIO.input(int(gpio))

cfile = "default.txt"
port = 5002
gpioattrs=[]
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("",port))
server_socket.listen(5)

try: 
   opts, args = getopt.getopt(sys.argv[1:],"c:p:")
except getopt.GetoptError:
   print 'RelaysServerTest -c <config file> -p <port number>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-p':
      port = arg
   if opt == '-c':
      cfile = arg

print "File di configurazione: ",cfile

ocfile = open(cfile)
line = ocfile.readline()
while len(line):
  gpioattr=line.split()
  print len(gpioattr), gpioattr
  if len(gpioattr)==4:
    gpioattrs.append(gpioattr)
  line =ocfile.readline()
print "end of file reached"
print gpioattrs

GPIO.setmode(GPIO.BCM)
for gpio, name, start, lock in gpioattrs:
   print gpio,name,start,lock
   GPIO.setup(int(gpio),GPIO.OUT)
   GPIO.output(int(gpio),start=="True")

print "Pronto sulla porta ", port

try: 
   while True:
       client_socket, address =server_socket.accept()
       print "Connection from ", address
       data = client_socket.recv(512)
       print "RECIEVED:" , data
       command=data.split()
       if len(command)>1:
         if command[0] == 'accendi':
            accensione_relay(int(command[1]))
            client_socket.send("accensione GPIO "+command[1]+" eseguita")
         if command[0] == 'spegni':
            spegnimento_relay(int(command[1]))
            client_socket.send("spegnimento GPIO "+command[1]+ " +eseguito")
       if command[0] == 'stato':
            stato_relays()
            client_socket.send("richiesta stato eseguita")
       client_socket.close()
except KeyboardInterrupt:
     print "Program interrupted"
  
except:
     print "Program aborted with unexpected error: ", sys.exc_info()[0]

finally:
   print "Cleaning up GPIO..."
   ret=GPIO.cleanup()
   print "GPIO cleaned up ",ret
   print "Closing socket..."   	
   ret=server_socket.close()
   print "socket closed ",ret 
