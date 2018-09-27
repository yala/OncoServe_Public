import os, shutil
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
sys.path.append(os.path.join(dirname(dirname(realpath(__file__))),'OncoNet'))
sys.path.append(os.path.join(dirname(dirname(realpath(__file__))), 'OncoData'))
sys.path.append(os.path.join(dirname(dirname(realpath(__file__))), 'OncoQueries'))
import sys
import oncoserve.logger
from flask import Flask
from flask import request, json, jsonify
import oncoserve.onconet_wrapper as onconet_wrapper
import oncoserve.oncodata_wrapper as oncodata_wrapper
import oncoserve.oncoqueries_wrapper as oncoqueries_wrapper
import pdb

ONCODATA_SUCCESS_MSG = 'OncoData- Successfully converted dicoms into pngs through OncoData'
ONCOQUERIES_SUCCESS_MSG = 'OncoQueries- Successfully obtained risk factors through OncoQueries'
ONCONET_SUCCESS_MSG = 'OncoNet- Succesfully got prediction from OncoNet for exam'
ONCOSERVE_FAIL_MSG = 'Error. Could not serve request. Exception: {}'
HTTP_200_OK = 200
HTTP_500_INTERNAL_SERVER_ERROR = 500
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.environ['LOGFILE']
CONFIG_NAME = os.environ['CONFIG_NAME']
app.config.from_object(CONFIG_NAME)
# create logger
logger = oncoserve.logger.get_logger('oncologger', LOG_FILE)

onconet_args = app.config['ONCONET_ARGS']
oncodata_args = app.config['ONCODATA_ARGS']
# Init onconet wrapper
onconet = onconet_wrapper.OncoNetWrapper(onconet_args, app.config['AGGREGATION'], logger)


@app.route('/serve', methods=['POST'])
def serve():
    '''
        API to serve a model from OncoNet
        Takes a list of dicom files, and a list of optional keys
        i.e { dicoms: [bytes, bytes, bytes], data: { optional metadata} }
        and returns:
            { prediction: Y, metadata: {}, model_name : NAME,
            oncoserve_version: X.X.X, onconet_version: X.X.X,
            oncodata_version: X.X.X}

        Prediction is the exam level prediction over dicoms.
        Model_name defines what predictor is running: i.e density, risk etc.
        Metadata is meant to contain things like MRN, ACCESSION and any
        additional metadata for object tracking.
        OncoServe_version is the version of the model deployment framework
        OncoNet_version is the version of the research model framework
        OncoData_version is the version of the dicom conversion framework

        The configuration of the model used to produce Y is set in the app configuration. See config.py for config objects.
    '''
    logger.info("Serving request...")
    response = {
                'model_name': app.config['NAME'],
                'oncoserve_version': app.config['ONCOSERVE_VERSION'],
                'onconet_version': app.config['ONCONET_VERSION'],
                'oncodata_version': app.config['ONCODATA_VERSION'],
                'log_file': LOG_FILE
                }
    try:
        dicoms = request.files.getlist('dicom')
        metadata = request.form
        response['metadata'] = metadata
        images = oncodata_wrapper.get_pngs(dicoms, oncodata_args, logger)
        logger.info(ONCODATA_SUCCESS_MSG)
        if onconet_args.use_risk_factors:
            assert 'mrn' in metadata
            assert 'accession' in metadata            
            risk_factor_vector = oncoqueries_wrapper.get_risk_factors(onconet_args, 
                                            metadata['mrn'], 
                                            metadata['accession'], 
                                            oncodata_args.temp_img_dir, 
                                            logger)
            logger.info(ONCOQUERIES_SUCCESS_MSG)
        else:
            risk_factor_vector = None
        y = onconet.process_exam(images, risk_factor_vector)
        logger.info(ONCONET_SUCCESS_MSG)
        msg = 'OK'
        response['prediction'] = y
        response['msg'] = msg
        return jsonify(response), HTTP_200_OK

    except Exception as e:
        msg = ONCOSERVE_FAIL_MSG.format(str(e))
        response['prediction'] = None
        response['msg'] = msg
        return jsonify(response), HTTP_500_INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    port = app.config['PORT']
    logger.info("Launching app at port {}".format(port))
    app.run(host='0.0.0.0', port=port)
