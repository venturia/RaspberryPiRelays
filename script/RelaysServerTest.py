#!/usr/bin/python

import sys
import socket
import getopt
import StringIO
import RPi.GPIO as GPIO

def trova_gpiostatus(gpioch):
    return next((st for st in gpiostatuses if st[0]==gpioch),[])

def decidi_relay(gpiost):
    print "decidere GPIO",gpiost[0],gpiost[4],gpiost[3]
    if gpiost[4]>=gpiost[3]:
        GPIO.output(gpiost[0],True)    
    else:
        GPIO.output(gpiost[0],False)    

def accensione_relay(gpiost):
    print "Accendo GPIO ",gpiost[0]
    gpiost[4]=gpiost[2]	
    decidi_relay(gpiost)

def abilitazione_bit_relay(gpiost,bit):
    print "Abilito bit",bit," GPIO ",gpiost[0]
    gpiost[4]= gpiost[4] | (2**bit & gpiost[2])	# in this way bits outside the mask are ignored
    decidi_relay(gpiost)

def spegnimento_relay(gpiost):
    print "Spengo GPIO ",gpiost[0]
    gpiost[4]=0	
    decidi_relay(gpiost)

def disabilitazione_bit_relay(gpiost,bit):
    print "Abilito bit",bit," GPIO ",gpiost[0]
    gpiost[4]= gpiost[4] & ((~(2**bit)) & gpiost[2]) # in this way bits outside the mask are ignored
    decidi_relay(gpiost)

def stato_relays(csock):
    print "Stampo stato"
    statusstring = StringIO.StringIO()
    for gpio,name,mask,oncond,status,lock in gpiostatuses:
       print>>statusstring, gpio,name,mask,oncond,status,lock,GPIO.input(gpio)
    csock.send(statusstring.getvalue())

cfile = "default.txt"
port = 5002
STATUSELEMENTS=6
gpioattrs=[]
gpiostatuses=[]
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
  if len(gpioattr)==STATUSELEMENTS:
    gpioattrs.append(gpioattr)
  line =ocfile.readline()
print "end of file reached"

GPIO.setmode(GPIO.BCM)
for gpio, name, mask, oncond, start, lock in gpioattrs:
   GPIO.setup(int(gpio),GPIO.OUT)
   gpiostatus=[int(gpio),name,int(mask),int(oncond),int(start),lock=="True"]
   print gpiostatus
   gpiostatuses.append(gpiostatus)
   GPIO.output(int(gpio),int(start)>=int(oncond))

print "Pronto sulla porta ", port

try: 
   while True:
       client_socket, address =server_socket.accept()
       print "Connection from ", address
       data = client_socket.recv(512)
       print "RECIEVED:" , data
       command=data.split()
       if len(command)>1:
          gpiost = trova_gpiostatus(int(command[1]))
          if len(gpiost)==STATUSELEMENTS:
             if len(command)>2:
                 gpiobit=2**int(command[2]) & gpiost[2]
                 if gpiobit>0:
                    if command[0] == 'abilita':
                        abilitazione_bit_relay(gpiost,int(command[2]))
                        client_socket.send("abilitazione bit %s GPIO %d eseguita" % (command[2], gpiost[0]))
                    if command[0] == 'disabilita':
                        disabilitazione_bit_relay(gpiost,int(command[2]))
                        client_socket.send("disabilitazione bit %s GPIO %d eseguito" % (command[2], gpiost[0]))
                 else:
                    client_socket("bit da (dis)abilitare non valido") 
             elif len(command)>1:
                if command[0] == 'accendi':
                    accensione_relay(gpiost)
                    client_socket.send("accensione GPIO %d eseguita" % gpiost[0])
                if command[0] == 'spegni':
                    spegnimento_relay(gpiost)
                    client_socket.send("spegnimento GPIO %d eseguito" % gpiost[0])
          else:
             client_socket.send("Numero porta GPIO non riconosciuto") 
       elif command[0] == 'stato':
            stato_relays(client_socket)
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
