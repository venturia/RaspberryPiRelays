# RaspberryPiRelays

Per i raspberry senza `systemd` bisogna mettere questa linea nel file di configurazione dei cron job (usando `sudo`):
`@reboot /home/pi/RaspberryPiRelays/script/RelaysServerTest.py --savedrestart -p 5002 -c /home/pi/RaspberryPiRelays/script/relays_rpi02.txt  >> /home/pi/log.txt 2>&1
`
