from flask import Flask

import os
import shutil
from datetime import datetime
from werkzeug import secure_filename
from flask import render_template, request, send_file
import word2html
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['JOBS_FOLDER'] = "jobs"


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
        # Make a folder under the job folder for this file
        file_dir = os.path.join(job_dir, os.path.splitext(
            secure_filename(file.filename))[0])
        os.makedirs(file_dir)
        new_path = os.path.join(file_dir, secure_filename(file.filename))
        file.save(new_path)
        converted_file = word2html.convert_to_html(new_path)
        copy_media_files(os.path.join(file_dir, 'media'), file_dir)
        new_html = correct_image_paths(open(converted_file, 'r'))
        with open(converted_file, 'wb') as f:
            f.write(new_html.prettify('utf-8'))
        print(converted_file)
    # Archive completed job and send the zip
    zip_file = shutil.make_archive(job_dir, 'zip', job_dir)
    return send_file(zip_file, as_attachment=True)


def copy_media_files(dir, dest_dir):
    for filename in os.listdir(dir):
        shutil.move(os.path.join(dir, filename), dest_dir)
    os.rmdir(dir)


def correct_image_paths(html_content):
    html = BeautifulSoup(html_content, 'html.parser')
    images = html.find_all('img')
    for image in images:
        if image.get('height'):
            del image['height']

        if image.get('width'):
            del image['width']
        image['max-width'] = '100%'
        image['src'] = os.path.basename(image['src'])
        print(image)
    html_content.close()
    return html
    # urls = [image['src'] for image in images]
    # print(urls)


if __name__ == '__main__':
    app.run(debug=True)
