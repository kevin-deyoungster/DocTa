from flask import Flask
import os

app = Flask(__name__)
app.config['JOBS_FOLDER'] = "{}/jobs".format(os.getcwd())
from app import routes
