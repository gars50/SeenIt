import os
import datetime
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello!</h1>"


#Run with
#.\env\Scripts\activate
#SET FLASK_APP=app.py
#flask --debug run