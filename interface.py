import os, shutil
import sys
import getopt
import logging
from flask import Flask
from flask import render_template, redirect, request, json, jsonify
from learning import analyzer
from werkzeug.utils import secure_filename

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config.from_object('config')
app.config.update(
    UPLOAD_FOLDER=os.path.join(APP_ROOT, 'static/uploads')
)

# create logger
logger = logging.getLogger('oncologger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('errors.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


@app.route('/')
def index():
    logger.info("Deleting previously uploaded files...")
    try:
        # Deletes previously uploaded files on refresh
        for files in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], files)
            if os.path.isfile(filepath):
                os.unlink(filepath)
        logger.info("Files successfully deleted!")
    except Exception as e:
        logger.error(str(e))
    return render_template('index.html')

@app.route('/serving', methods=['POST'])
def serving():
    logger.info("Serving request...")
    try:
        data = request.files.getlist('file')
        for img in data:
            filename = str(secure_filename(img.filename))
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response = analyzer(data, app.config['MODEL'], app.config['AGGREGATION'])
        logger.info("Files successfully served!")
        return jsonify(response)
    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": str(e)})
