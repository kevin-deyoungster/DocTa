from app import app
import os
from flask import render_template, request, send_file
from werkzeug import secure_filename


@app.route('/')
@app.route('/index')
def index():
    title = "Chalkboard Education DOCta v1.0"
    return render_template('index.html', title=title)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    f = request.files.getlist("file[]")
    print(len(f))
    file = f[0]
    # for file in f:
    new_path = os.path.join(
        app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(new_path)

    return send_file(convert_to_html(new_path), as_attachment=True)


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
