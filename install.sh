#!/bin/bash

WEBDIR=/var/www/html
CGIDIR=/usr/lib/cgi-bin

# copy the web pages in the web server subdirectory "relays"

if [ ! -d "${WEBDIR}/relays" ]
then
  echo "creating ${WEBDIR}/relays directory"
  mkdir ${WEBDIR}/relays
fi
echo "copying php scripts"
cp -v webpages/*.php ${WEBDIR}/relays/.
echo "copying html files"
cp -v webpages/*.html ${WEBDIR}/relays/.
if [ ! -d "${CGIDIR}/relays" ]
then
  echo "creating ${CGIDIR}/relays directory"
  mkdir ${CGIDIR}/relays
fi
echo "copying py files"
cp -v webpages/*.py ${CGIDIR}/relays/.

