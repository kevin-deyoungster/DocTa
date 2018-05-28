from app import app
import os
from flask import render_template, request, send_file
from werkzeug import secure_filename
from datetime import datetime
import shutil
from app import word2html


@app.route('/')
@app.route('/index')
def index():
    title = "Chalkboard Education DOCta v1.0"
    return render_template('index.html', title=title)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    f = request.files.getlist("file[]")
    time_stamp = str(datetime.now().strftime("%m-%d-%Y.%H-%M-%S"))
    time_stamp_dir = os.path.join(
        app.config['UPLOAD_FOLDER'], time_stamp)
    os.makedirs(time_stamp_dir)

    # Convert each file
    for file in f:
        new_path = os.path.join(time_stamp_dir, secure_filename(file.filename))
        file.save(new_path)
        word2html.convert_to_html(new_path)

    zip_file = os.path.join(time_stamp_dir, time_stamp)
    return send_file(shutil.make_archive(zip_file, 'zip', time_stamp_dir), as_attachment=True)
