import os, shutil
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
sys.path.append(os.path.join(dirname(dirname(realpath(__file__))),'OncoNet'))
sys.path.append(os.path.join(dirname(dirname(realpath(__file__))), 'OncoData'))
import sys
import getopt
import oncoserve.logger
from flask import Flask
from flask import render_template, redirect, request, json, jsonify
import oncoserve.onconet_wrapper as onconet_wrapper
import oncoserve.oncodata_wrapper as oncodata_wrapper
import pdb

ONCODATA_SUCCESS_MSG = 'Successfully converted dicoms into pngs through OncoData'
ONCONET_SUCCESS_MSG = 'Succesfully got prediction from OncoNet for exam'
ONCOSERVE_FAIL_MSG = 'Error. Could not serve request. Exception: {}'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config.from_object('config.DensityConfig')

# create logger
logger = oncoserve.logger.get_logger('oncologger', app.config['LOGFILE'])

onconet_args = app.config['ONCONET_ARGS']
oncodata_args = app.config['ONCODATA_ARGS']
# Init onconet wrapper
onconet = onconet_wrapper.OncoNetWrapper(onconet_args, app.config['AGGREGATION'], logger)


@app.route('/serve', methods=['POST'])
def serve():
    '''
        API to serve a model from OncoNet
        Takes a list of dicom files, and a list of optional keys
        i.e { dicoms: [bytes, bytes, bytes], additional: {} }
        and returns:
            { prediction: Y, additional: {}}

        Additional is meant to contain things like MRN, ACCESSION and any
        additional metadata for object tracking. The configuration of the model used to produce Y is set in the app configuration.
    '''
    logger.info("Serving request...")
    try:
        dicoms = request.files.getlist('dicom')
        additional = request.form
        images = oncodata_wrapper.get_pngs(dicoms, oncodata_args, logger)
        logger.info(ONCODATA_SUCCESS_MSG)
        y = onconet.process_exam(images)
        logger.info(ONCONET_SUCCESS_MSG)
        msg = 'OK'
        response = {'prediction': y, 'additional': additional, 'msg':msg}
        return jsonify(response)

    except Exception as e:
        msg = ONCOSERVE_FAIL_MSG.format(str(e))
        response = {'prediction': None, 'additional': additional, 'msg':msg}
        logger.error(msg)
        return jsonify(response)

if __name__ == '__main__':
    port = 5000
    logger.info("Launching app at port {}".format(port))
    app.run(host='0.0.0.0', port=port)
