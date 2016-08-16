import json
import os
import sys
import logging
from flask import Flask
from mongoengine import *
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS', 'config.DevelopmentConfig'))
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
db = MongoEngine(app)


import views
import models
import forms