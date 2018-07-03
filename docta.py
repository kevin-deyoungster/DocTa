import os
import shutil
from datetime import datetime
from werkzeug import secure_filename
from flask import Flask, render_template, request, send_file
import word2html
from bs4 import BeautifulSoup
from os import path
import data
import html_polisher

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', title=data.HTML_HEADING)


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_docs = request.files.getlist("file[]")

    # Create Job Folder
    time_stamp = str(datetime.now().strftime("%m-%d-%Y.%H-%M-%S"))
    job_dir = path.join(data.JOBS_FOLDER, time_stamp)
    os.makedirs(job_dir)

    # Convert each file
    for file in uploaded_docs:
        # Make a folder under the job folder for this file
        file_dir = path.join(job_dir, path.splitext(
            secure_filename(file.filename))[0])
        print(path.splitext(
            secure_filename(file.filename)))
        os.makedirs(file_dir)
        new_path = path.join(file_dir, secure_filename(file.filename))
        file.save(new_path)
        converted_file = word2html.convert_to_html(new_path)
        copy_media_files(path.join(file_dir, 'media'), file_dir)
        html_polisher.polish(converted_file)

        # Rename as index.html
        os.rename(converted_file, path.join(
            path.dirname(converted_file), 'index.html'))
        print(converted_file)

    # Archive completed job and send the zip
    zip_file = shutil.make_archive(job_dir, 'zip', job_dir)
    shutil.rmtree(job_dir)
    return send_file(zip_file, as_attachment=True)


def copy_media_files(dir, dest_dir):
    for filename in os.listdir(dir):
        shutil.move(path.join(dir, filename), dest_dir)
    os.rmdir(dir)


if __name__ == '__main__':
    app.run(debug=True)
