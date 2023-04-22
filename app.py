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

@app.route("/test")
def test():
    return render_template("test.html", testName = testName)

@app.route("/about")
def about():
    return render_template("about.html")


#Run with
#.\env\Scripts\activate
#SET FLASK_APP=app.py
#flask --debug run