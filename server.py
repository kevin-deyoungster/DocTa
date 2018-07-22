import data
import shutil
from flask_cors import CORS
from convertor import Convert
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
CORS(app)

# Clear Jobs Directory
if not data.PERSIST_JOBS:
    shutil.rmtree(data.JOBS_FOLDER, ignore_errors=True)


@app.route('/')
def index():
    return render_template('index.html', title=data.HTML_HEADING, version=data.VERSION)


@app.route('/convert', methods=['POST'])
def upload():
    uploaded_docs = request.files.getlist("file[]")
    zip_of_job = Convert.convert(uploaded_docs, data.JOBS_FOLDER)
    return send_file(zip_of_job, attachment_filename='Converted.zip', as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
