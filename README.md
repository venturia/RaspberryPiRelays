# RaspberryPiRelays

Per i raspberry senza `systemd` bisogna mettere questa linea nel file di configurazione dei cron job (usando `sudo`):
`@reboot /home/pi/RaspberryPiRelays/script/RelaysServerTest.py --savedrestart -p 5002 -c /home/pi/RaspberryPiRelays/script/relays_rpi02.txt  >> /home/pi/log.txt 2>&1
`
Per i raspberry con `systemd` bisogna attivare il servizio al boot con:
`sudo systemctl enable relayserver`

Per segnalare lo stato dell'allarme presenze con i LED occorre eseguire:
`./RaspberryPiRelays/script/presencealarmChecker.sh RaspberryPiRelays/script/presencealarmConfig.txt &`

per funzionare bisogna installare inotify-tools:

sudo apt-get install inotify-tools
