#!/usr/bin/python

import sys
import socket
import RPi.GPIO as GPIO

def accensione_relay(gpioch):
    print "Accendo GPIO ",gpioch
    GPIO.output(gpioch,True)    

def spegnimento_relay(gpioch):
    print "Spengo GPIO ",gpioch
    GPIO.output(gpioch,False)    

def stampa_stato():
    print "Stampo stato"


port = 5002
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("",port))
server_socket.listen(5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,False)    
GPIO.setup(22,GPIO.OUT)
GPIO.output(22,False)    
GPIO.setup(27,GPIO.OUT)
GPIO.output(27,False)    
GPIO.setup(14,GPIO.OUT)
GPIO.output(14,False)    
GPIO.setup(15,GPIO.OUT)
GPIO.output(15,False)    
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,False)    
GPIO.setup(24,GPIO.OUT)
GPIO.output(24,False)    
GPIO.setup(25,GPIO.OUT)
GPIO.output(25,False)    

print "Pronto sulla porta ", port

try: 
   while True:
       client_socket, address =server_socket.accept()
       print "Connection from ", address
       data = client_socket.recv(512)
       print "RECIEVED:" , data
       command=data.split()
       print command
       if command[0] == 'accendi':
          accensione_relay(int(command[1]))
       if command[0] == 'spegni':
          spegnimento_relay(int(command[1]))

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
