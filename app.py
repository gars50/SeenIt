from markupsafe import escape
from flask import Flask
from configparser import ConfigParser

app = Flask(__name__)

config = ConfigParser()
config.read("config.ini")

testName = config.get("DEFAULT", "testName")

@app.route("/")
def index():
    return "<h1>Hello!</h1>"

@app.route("/test")
def test():
    return '<h1>{}</h1>'.format(escape(testName.capitalize()))


#Run with
#.\env\Scripts\activate
#SET FLASK_APP=app.py
#flask --debug run