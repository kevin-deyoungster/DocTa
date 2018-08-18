from config import setup
from config import data
from modules import convertor
from flask_cors import CORS
from flask import Flask, render_template, request, send_file
import webbrowser

# A few background checks
setup.initiate()
webbrowser.open("http://localhost:5000")

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html", title=data.HTML_HEADING, version=data.VERSION)


@app.route("/convert", methods=["POST"])
def upload():
    uploaded_docs = request.files.getlist("file[]")
    zip_of_job = convertor.convert(uploaded_docs, data.JOBS_FOLDER, ["@", "~"])
    return send_file(
        zip_of_job, attachment_filename=data.ZIP_DEFAULT_NAME, as_attachment=True
    )


if __name__ == "__main__":
    app.run(host=data.HOST, debug=data.DEBUG_SERVER)
