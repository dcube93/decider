Repo for VCID PA decider Flask App

Die App wird mittels decider.py gestartet. 
Die Python Anforderungen sind in der requirements.txt Datei zu finden.

Folgende Befehle sind nötig um die Ausgangslage zu schaffen, dass die Applikation betrieben werden kann:

Installiert Python Pakete sofern nicht vorhanden: 
sudo apt install python3 python3-pip python3-venv python3-dev -y

Installiert Anforderungen aus requirements.txt
pip install -r requirements.txt

Installiert und startet MariaDB Server:
sudo apt install mariadb-server
sudo systemctl start mariadb.service

Installiert Supervisor
sudo apt install supervisor

Erstellt Konfigurationsdatei für Supervisor
sudo nano /etc/supervisor/conf.d/decider.conf
Inhalt:
[program:decider]
command=/home/azureuser/project/decider/venv/bin/gunicorn -b 0.0.0.0:8000 -w 4 app:app
directory=/home/azureuser/project/decider
user=azureuser
autostart=true
autorestart=true
stopasgroup=true

