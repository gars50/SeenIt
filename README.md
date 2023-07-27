SeenIt
Web service that allows your users to delete their media once they have watched it.
This connects to Ombi, Radarr and Sonarr to delete the requests in Ombi, and the movies/series from Radarr/Sonarr. This is to allow users to submit the same series again afterwards.
I am learning Python Flask with this, so do not expect high quality code!

Setup:
1. 
apt install python3
git clone https://github.com/gars50/SeenIt.git
python3 -m venv ~/env/venv
source ~/env/venv/bin/activate
cd SeenIt
pip install -r requirements.txt
pip install gunicorn

2. Export necessary environment variables

export SECRET_KEY="XXXXXXXXXXXXXXXXXX"
export DATABASE_URI="XXXXXXXXXXXXXXXXXXXXXX"
export MAIL_USERNAME="xxxxxx@xxxxxx.xxx"
export MAIL_PASSWORD="xxxxxxxxxxxx"