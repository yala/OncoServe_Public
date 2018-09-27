import os
import uuid
import oncoserve.logger
from onconet.utils.risk_factors import RiskFactorVectorizer
import json
import subprocess
import pdb


FAIL_TO_SAVE_METADATA_MESSAGE = 'OncoQueries- Fail to save metadata json for ssn: {}, accession: {}. Caused Exception {} with args: {}'
FAIL_TO_SAVE_RISK_METADATA_MESSAGE = 'OncoQueries- Fail to save risk_metadata json for ssn: {}, accession: {}. Caused Exception {} with args: {}'
FAIL_TO_GET_RISK_VECTOR_MESSAGE = 'OncoQueries- Fail to get risk_factor_vector given metadatas for ssn: {}, accession: {}. Caused Exception {} with args: {}'
SUCCESS_RISK_VEC_MESSAGE = 'OncoQueries- Succesffuly obtained risk_factor_vector for ssn: {}, accession: {} with args: {}'



def risk_factor_vector(args, ssn, exam, json_dir, logger):
    '''
    args:
        - args:
        - ssn:
        - exam:
        - json_dir:
        - logger:
    returns:
        - risk_factor_vector:  
    '''
    try:
        os.makedirs(args.temp_img_dir)
    except Exception as e:
        pass
    args.metadata_path = "{}.json".format(os.path.join(json_dir, str(uuid.uuid4())))
    args.risk_factor_metadata_path = "{}.json".format(os.path.join(json_dir, str(uuid.uuid4())))
    # Write current request to a file to use as a metadata path
    metadata_json = [{'ssn':ssn, 'accessions':[{'accession':exam}]}]

    try:
        json.dump(metadata_json, open(args.metadata_path,'w'))
    except Exception as e:
        if os.path.exists(args.metadata_path):
            os.remove(args.metadata_path)
        err_msg = FAIL_TO_SAVE_METADATA_MESSAGE.format(ssn, exam, e, args)
        logger.error(err_msg)
        raise Exception(err_msg)

    # Call OncoQueries with specifc SSN and ACCESSION to get risk factor metadata json
    oncoqueries_command = 'python OncoQueries/scripts/from_db/create_risk_factor_metadata.py --save_path {} --patient_mrn {} --patient_accession {}'.format(
                                                args.risk_factor_metadata_path, ssn, exam)
    try:
        subprocess.call(oncoqueries_command, shell=True)
    except Exception as e:
        for path in [args.metadata_path, args.risk_factor_metadata_path]
            if os.path.exists(path):
                os.remove(path)
        err_msg = FAIL_TO_SAVE_RISK_METADATA_MESSAGE.format(ssn, exam, e, args)
        logger.error(err_msg)
        raise Exception(err_msg)

    # Load risk factor vector from metadata file and del metadata json
    try:
        risk_factor_vectorizer = RiskFactorVectorizer(args)
        sample = {'ssn': ssn, 'exam': exam}
        risk_factor_vector = risk_factor_vectorizer.get_risk_factors_for_sample(sample)
        logger.info(SUCCESS_RISK_VEC_MESSAGE.format(ssn, exam, args))
        return risk_factor_vector
    except Exception as e:
        for path in [args.metadata_path, args.risk_factor_metadata_path]
            if os.path.exists(path):
                os.remove(path)
        err_msg = FAIL_TO_GET_RISK_VECTOR_MESSAGE.format(ssn, exam, e, args)
        logger.error(err_msg)
        raise Exception(err_msg)    



