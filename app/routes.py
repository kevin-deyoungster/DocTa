from app import app
import os
from flask import render_template, request, send_file
from werkzeug import secure_filename
from datetime import datetime
import shutil


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
        convert_to_html(new_path)

    zip_file = os.path.join(time_stamp_dir, time_stamp)
    return send_file(shutil.make_archive(zip_file, 'zip', time_stamp_dir), as_attachment=True)


def convert_to_html(filename):
    import sys
    try:
        import pypandoc
        from tidylib import tidy_document
    except ImportError:
        print("\n\nRequires pypandoc and pytidylib. See requirements.txt\n\n")

    # Do the conversion with pandoc
    output = pypandoc.convert(filename, 'html')

    # Clean up with tidy...
    output, errors = tidy_document(output,  options={
        'numeric-entities': 1,
        'tidy-mark': 0,
        'wrap': 80,
    })
    print(errors)

    # replace smart quotes.
    output = output.replace(u"\u2018", '&lsquo;').replace(u"\u2019", '&rsquo;')
    output = output.replace(u"\u201c", "&ldquo;").replace(u"\u201d", "&rdquo;")

    # write the output
    filename, ext = os.path.splitext(filename)
    filename = "{0}.html".format(filename)
    with open(filename, 'w') as f:
        # Python 2 "fix". If this isn't a string, encode it.
        if type(output) is not str:
            output = output.encode('utf-8')
        f.write(output)

    return filename
