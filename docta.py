from flask import Flask

import os
import shutil
from datetime import datetime
from werkzeug import secure_filename
from flask import render_template, request, send_file
import word2html

app = Flask(__name__)
app.config['JOBS_FOLDER'] = "/home/ubuntu/flaskapp/jobs"


@app.route('/')
def index():
    title = "Chalkboard Education DOCta v1.0"
    return render_template('index.html', title=title)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    files = request.files.getlist("file[]")

    # Create Job Folder
    time_stamp = str(datetime.now().strftime("%m-%d-%Y.%H-%M-%S"))
    job_dir = os.path.join(
        app.config['JOBS_FOLDER'], time_stamp)

    os.makedirs(job_dir)

    # Convert each file
    for file in files:
        new_path = os.path.join(job_dir, secure_filename(file.filename))
        file.save(new_path)
        word2html.convert_to_html(new_path)

    # Archive completed job and send the zip
    zip_file = shutil.make_archive(job_dir, 'zip', job_dir)
    return send_file(zip_file, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
