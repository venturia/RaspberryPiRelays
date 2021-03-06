#!/usr/bin/python -u

import os
import signal
import sys
import socket
import getopt
import StringIO
import RPi.GPIO as GPIO

class GracefulSigTerm(Exception):
    pass

def sigterm_handler(signum,frame):
    raise GracefulSigTerm()

def trova_gpiostatus(gpioch):
    if gpioch.isdigit():
      return next((st for st in gpiostatuses if st[0]==int(gpioch)),[])
    else:
      return next((st for st in gpiostatuses if st[1]==gpioch),[])

def decidi_relay(gpiost):
    print "decidere GPIO",gpiost[0],gpiost[4],gpiost[3]
    if gpiost[4]>=gpiost[3]:
        GPIO.output(gpiost[0],True)    
    else:
        GPIO.output(gpiost[0],False)    

def accensione_relay(gpiost):
    print "Accendo GPIO ",gpiost[0]
    gpiost[4]=2**gpiost[2]-1	
    decidi_relay(gpiost)

def abilitazione_bit_relay(gpiost,bit):
    print "Abilito bit",bit," GPIO ",gpiost[0]
    gpiost[4]= gpiost[4] | (2**bit & 2**gpiost[2]-1)	# in this way bits outside the mask are ignored
    decidi_relay(gpiost)

def spegnimento_relay(gpiost):
    print "Spengo GPIO ",gpiost[0]
    gpiost[4]=0	
    decidi_relay(gpiost)

def disabilitazione_bit_relay(gpiost,bit):
    print "Abilito bit",bit," GPIO ",gpiost[0]
    gpiost[4]= gpiost[4] & ((~(2**bit)) & 2**gpiost[2]-1) # in this way bits outside the mask are ignored
    decidi_relay(gpiost)

def set_bit_relay(gpiost,bitmask):
    print "Configuro bit mask ",bitmask," GPIO ",gpiost[0]
    gpiost[4]= bitmask & (2**gpiost[2]-1) # in this way bits outside the mask are ignored
    decidi_relay(gpiost)

def stato_relay(csock,gpiost):
    print "Stampo stato GPIO ",gpiost[0]
    statusstring = StringIO.StringIO()
    print>>statusstring, "$0$ *richiesta stato GPIO ",gpiost[0]," eseguita*"
    print>>statusstring, GPIO.input(gpiost[0])
    csock.send(statusstring.getvalue())

def stato_relays(csock):
    print "Stampo stato"
    statusstring = StringIO.StringIO()
    print>>statusstring, "$0$ *richiesta stato eseguita*"
    for gpio,name,mask,oncond,status,lock in gpiostatuses:
       print>>statusstring, gpio,name,mask,oncond,status,lock,GPIO.input(gpio)
    csock.send(statusstring.getvalue())

signal.signal(signal.SIGTERM, sigterm_handler)

cfile = "default.txt"
savedfile = os.path.dirname(sys.argv[0])+"/status.saved"
port = 5002
savedrestart=False
STATUSELEMENTS=6
gpioattrs=[]
gpiostatuses=[]

try: 
   opts, args = getopt.getopt(sys.argv[1:],"c:p:",['savedrestart'])
except getopt.GetoptError:
   print 'RelaysServerTest -c <config file> -p <port number>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-p':
      port = int(arg)
   if opt == '-c':
      cfile = arg
   if opt == '--savedrestart':
      savedrestart=True

print "File di configurazione: ",cfile
if savedrestart & os.path.exists(savedfile):
   cfile=savedfile
   print "Utilizzo file con configurazione precedente" 

ocfile = open(cfile)
line = ocfile.readline()
while len(line):
  gpioattr=line.split()
  print len(gpioattr), gpioattr
  if len(gpioattr)==STATUSELEMENTS:
    gpioattrs.append(gpioattr)
  line =ocfile.readline()
print "end of file reached"
ocfile.close()

GPIO.setmode(GPIO.BCM)
for gpio, name, mask, oncond, start, lock in gpioattrs:
   if (int(oncond) > 2**int(mask)-1 ) | (int(start) > 2**int(mask)-1):
      print "Configurazione non corretta: ",mask,oncond,start
      sys.exit(2)
   GPIO.setup(int(gpio),GPIO.OUT)
   gpiostatus=[int(gpio),name,int(mask),int(oncond),int(start),int(lock)]
   print gpiostatus
   gpiostatuses.append(gpiostatus)
   GPIO.output(int(gpio),int(start)>=int(oncond))

print "Pronto sulla porta ", port

try: 
   server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   server_socket.bind(("",port))
   server_socket.listen(5)
   while True:
       client_socket, address =server_socket.accept()
       data = client_socket.recv(512)
       print "RECEIVED from ",address, " :" , data
       command=data.split()
       if len(command)>1:
          gpiost = trova_gpiostatus(command[1])
          if len(gpiost)==STATUSELEMENTS:
             if len(command)>2:
                 if command[2].isdigit() :
                    if command[0] == 'abilita':
                        gpiobit=2**int(command[2]) & 2**gpiost[2]-1
                        if gpiobit>0:
                           abilitazione_bit_relay(gpiost,int(command[2]))
                           client_socket.send("$0$ *abilitazione bit %s GPIO %d eseguita*" % (command[2], gpiost[0]))
                        else:
                           print "bit da abiltare non valido"
                           client_socket.send("$21$ *bit da (dis)abilitare non valido*") 
                    if command[0] == 'disabilita':
                        gpiobit=2**int(command[2]) & 2**gpiost[2]-1
                        if gpiobit>0:
                           disabilitazione_bit_relay(gpiost,int(command[2]))
                           client_socket.send("$0$ *disabilitazione bit %s GPIO %d eseguita*" % (command[2], gpiost[0]))
                        else:
                           print "bit da disabiltare non valido"
                           client_socket.send("$21$ *bit da (dis)abilitare non valido*") 
                    if command[0] == 'configura':
                        if int(command[2]) == (int(command[2]) & 2**gpiost[2]-1):
                           set_bit_relay(gpiost,int(command[2]))
                           client_socket.send("$0$ *configura bits %s GPIO %d eseguita*" % (command[2], gpiost[0]))
                        else:
                           print "bitmask da configurare non valida"
                           client_socket.send("$22$ *bitmask %s non valida per GPIO %d*" % (command[2], gpiost[0])) 
                 else:
                     print "bit/bimask non intero"
                     client_socket.send("$23$ *bit o bitmask non intero: %s" % command[2])
             elif len(command)>1:
                if command[0] == 'accendi':
                    accensione_relay(gpiost)
                    client_socket.send("$0$ *accensione GPIO %d eseguita*" % gpiost[0])
                if command[0] == 'spegni':
                    spegnimento_relay(gpiost)
                    client_socket.send("$0$ *spegnimento GPIO %d eseguito*" % gpiost[0])
                if command[0] == 'stato':
                    stato_relay(client_socket,gpiost)
          else:
             client_socket.send("$31$ *Numero o nome porta GPIO non riconosciuto: %s*" % command[1]) 
       elif command[0] == 'stato':
            stato_relays(client_socket)
       client_socket.close()
except KeyboardInterrupt:
     print "Program interrupted"
  
except GracefulSigTerm:
     print "Server terminated by SIGTERM"

except:
     print "Program aborted with unexpected error: ", sys.exc_info()[0]

finally:
   print "Cleaning up GPIO..."
   ret=GPIO.cleanup()
   print "GPIO cleaned up ",ret
   print "Closing socket..."   	
   ret=server_socket.close()
   print "socket closed ",ret 
   print "ready to save the status in ",savedfile
   sout = open(savedfile,"w")
   for gpio,name,mask,oncond,status,lock in gpiostatuses:
       print>>sout, gpio,name,mask,oncond,status,lock
   	
