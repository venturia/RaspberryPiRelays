# RaspberryPiRelays

Per i raspberry senza `systemd` bisogna mettere questa linea nel file di configurazione dei cron job (usando `sudo`):
`@reboot /home/pi/RaspberryPiRelays/script/RelaysServerTest.py --savedrestart -p 5002 -c /home/pi/RaspberryPiRelays/script/relays_rpi02.txt  >> /home/pi/log.txt 2>&1`

Per i raspberry con `systemd` bisogna attivare i servizi al boot con:
`sudo systemctl enable relayserver`

Per segnalare lo stato dell'allarme presenze con i LED occorre eseguire:
`./RaspberryPiRelays/script/presencealarmChecker.sh RaspberryPiRelays/script/presencealarmConfig.txt &`
quando systemd non e' disponibile. Altrimenti viene installato automaticamente come unit `systemd` e per attivarlo al boot occorre eseguire il comando:
`sudo systemctl enable presencealarmchecker`

Per funzionare bisogna installare inotify-tools:
`sudo apt-get install inotify-tools`
