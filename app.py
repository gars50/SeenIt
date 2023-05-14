from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')





@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mymovies")
def mymovies():
    return render_template("mymovies.html")

@app.route("/myshows")
def myshows():
    return render_template("myshows.html")

@app.route("/abandonnedmovies")
def abandonnedmovies():
    return render_template("abandonnedmovies.html")

@app.route("/abandonnedshows")
def abandonnedshows():
    return render_template("abandonnedshows.html")


#Run with
#.\venv\Scripts\activate
#SET FLASK_APP=app.py
#flask --debug run

#Save pip requirements 
#pip freeze > requirements.txt