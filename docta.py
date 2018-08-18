from config import setup
from config import data

LOG_TAG = "DocTa"
setup.initiate(data)

from modules import convertor
from flask_cors import CORS
from flask import Flask, render_template, request, send_file
import webbrowser
import logging

webbrowser.open("http://localhost:5000")

app = Flask(__name__, template_folder="public", static_folder="public")
CORS(app)
app.logger.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route("/")
def index():
    return render_template("index.html", title=data.HTML_HEADING, version=data.VERSION)


@app.route("/convert", methods=["POST"])
def upload():
    uploaded_files = request.files.getlist("file[]")
    # Debug
    filenames = ", ".join(
        [
            f"'{str(index+1)}. {f.filename[:-5]}'"
            for index, f in enumerate(uploaded_files)
        ]
    )
    print(f"\n[{LOG_TAG}]: Converting {len(uploaded_files)} Files: {filenames}")

    zip_of_job = convertor.convert(uploaded_files, data.JOBS_FOLDER)

    return send_file(
        zip_of_job, attachment_filename=data.ZIP_DEFAULT_NAME, as_attachment=True
    )


if __name__ == "__main__":
    app.run(host=data.HOST, debug=data.DEBUG_SERVER)
