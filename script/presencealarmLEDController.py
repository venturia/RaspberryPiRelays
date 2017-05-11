#! /usr/bin/python

import relaylib
import os
import getopt
import sys

cfile = "default.txt"
try: 
   opts, args = getopt.getopt(sys.argv[1:],"c:")
except getopt.GetoptError:
   print 'presencealarmLEDController -c <config file>'
   sys.exit(2)
for opt, arg in opts:
   if opt == '-c':
      cfile = arg

clines = []
if os.path.exists(cfile):
   ocfile = open(cfile)
   line = ocfile.readline()
   while len(line):
     cline=line.split()
     if len(cline)==4:
       clines.append(cline)
     line = ocfile.readline()
   ocfile.close()
else:
   print 'No cfg file'
   sys.exit(2)

if os.path.isfile("/var/apache/enabled_alarm"):
   for node,port,gpioch,bit in clines:
      relaylib.abilita_bit(node,int(port),int(gpioch),int(bit))
else:
   for node,port,gpioch,bit in clines:
      relaylib.disabilita_bit(node,int(port),int(gpioch),int(bit))


