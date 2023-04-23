from markupsafe import escape
from flask import Flask, render_template
from configparser import ConfigParser

app = Flask(__name__)

config = ConfigParser()
config.read("config.ini")

testName = config.get("DEFAULT", "testName")
secretKey = config.get("DEFAULT", "secretKey")
app.config["SECRET_KEY"] = secretKey





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
#.\env\Scripts\activate
#SET FLASK_APP=app.py
#flask --debug run