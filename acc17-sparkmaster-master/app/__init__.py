# app/__init__.py

# third-party imports
from flask import Flask
import os

# local imports
from config import app_config


config_name = os.getenv('FLASK_CONFIG')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')

from app.controllers import *

