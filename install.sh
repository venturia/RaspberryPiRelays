#!/bin/bash

WEBDIR=/var/www/html
CGIDIR=/usr/lib/cgi-bin
SYSTEMDLIB=/lib/systemd/system
SERVERPORT=5002
SERVERCONFIGFILE="relays_rpi05.txt"

read -p "web server file directory [$WEBDIR]" chosenwebdir

if [ ${#chosenwebdir} != 0 ]; then
  WEBDIR=$chosenwebdir
fi
read -p "Server port [$SERVERPORT]" chosenserverport

if [ ${#chosenserverport} != 0 ]; then
  SERVERPORT=$chosenserverport
fi
read -p "Server configuration file [$SERVERCONFIGFILE]" chosenconfigfile

if [ ${#chosenconfigfile} != 0 ]; then
  SERVERCONFIGFILE=$chosenconfigfile
fi

echo "Web page file directory $WEBDIR"
echo "Server port $SERVERPORT"
echo "Server configuration file $SERVERCONFIGFILE"
echo "Installation directory ${PWD}"

# copy the web pages in the web server subdirectory "relays"

if [ ! -d "${WEBDIR}/relays" ]
then
  echo "creating ${WEBDIR}/relays directory"
  mkdir ${WEBDIR}/relays
fi
echo "copying html files"
cp -v webpages/controllo_relays.html ${WEBDIR}/relays/.

if [ ! -d "${CGIDIR}/relays" ]
then
  echo "creating ${CGIDIR}/relays directory"
  mkdir ${CGIDIR}/relays
fi
echo "copying py files"
sed 's:INSTALLATIONDIRECTORY:'${PWD}':g' webpages/accensione_relays.py > ${CGIDIR}/relays/accensione_relays.py
sed 's:INSTALLATIONDIRECTORY:'${PWD}':g' webpages/spegnimento_relays.py > ${CGIDIR}/relays/spegnimento_relays.py
sed 's:INSTALLATIONDIRECTORY:'${PWD}':g' webpages/configura_bitmask.py > ${CGIDIR}/relays/configura_bitmask.py
sed 's:INSTALLATIONDIRECTORY:'${PWD}':g' webpages/stato_relays.py > ${CGIDIR}/relays/stato_relays.py
#cp -v webpages/*.py ${CGIDIR}/relays/.

# prepare and copy the configuration file of thr service for systemd

echo "Preparing the configuration file for systemd"
sed 's:INSTALLATIONDIRECTORY:'${PWD}':g;s:SERVERPORT:'${SERVERPORT}':g;s:SERVERCONFIGFILE:'${SERVERCONFIGFILE}':g' relayserver.service > ${SYSTEMDLIB}/relayserver.service
systemctl daemon-reload
systemctl stop relayserver.service
systemctl start relayserver.service

