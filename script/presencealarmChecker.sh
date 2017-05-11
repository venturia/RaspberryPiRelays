#!/bin/bash

while [ 1 -eq 1 ]; do
  echo "Checking alarm file"
  /home/pi/RaspberryPiRelays/script/presencealarmLEDController.py -c $1
  inotifywait  -e create,delete /var/apache
done
