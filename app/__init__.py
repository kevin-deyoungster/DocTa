from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/media/kevin/Windows/Users/kaminoshinyu/Desktop/Chalkboard/DOCta/temp"

from app import routes
