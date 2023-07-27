SeenIt
Web service that allows your users to delete their media once they have watched it.
This connects to Ombi, Radarr and Sonarr to delete the requests in Ombi, and the movies/series from Radarr/Sonarr. This is to allow users to submit the same series again afterwards.
I am learning Python Flask with this, so do not expect high quality code!

Setup:
1. Install the necessary requirements

```
apt install python3
cd ~
git clone https://github.com/gars50/SeenIt.git
cd SeenIt
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

2. Configure necessary environment variables

```
export SECRET_KEY="XXXXXXXXXXXXXXXXXX"
export DATABASE_URI="XXXXXXXXXXXXXXXXXXXXXX"
export MAIL_USERNAME="xxxxxx@xxxxxx.xxx"
export MAIL_PASSWORD="XXXXXXXXXXXXXXXXXX"
```

3. Prep the database

```
flask db init
flask db migrate -m "Initial Commit"
flask db upgrade
```

4. Start the service and confirm it works

```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```


Systemd Service :
1. Configure systemd service
```
touch /etc/systemd/system/seenit.service
```
```
[Unit]
Description=Gunicorn instance to serve SeenIt
After=network.target

[Service]
User=YOURUSER
Group=www-data
WorkingDirectory=/home/YOURUSER/SeenIt
Environment="PATH=/home/YOURUSER/SeenIt/venv/bin"
ExecStart=/home/YOURUSER/SeenIt/venv/bin/gunicorn --workers 3 --bind unix:SeenIt.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

2. Put environment variables in the service
```
[Service]
Environment="SECRET_KEY=XXXXXXXXXXXXXXXXXX"
Environment="DATABASE_URI=XXXXXXXXXXXXXXXXXX"
Environment="MAIL_USERNAME=xxxx@xxxxx.xxxxx"
Environment="MAIL_PASSWORD=XXXXXXXXXXXXXXXXXX"
```

3. Start and enable the service
```
systemctl enable seenit
service seenit start
```

NGINX Reverse Proxy :
```
nano /etc/nginx/sites-available/seenit
```
```
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/YOURUSER/SeenIt/SeenIt.sock;
    }
}
```
```
ln -s /etc/nginx/sites-available/seenit /etc/nginx/sites-enabled
```