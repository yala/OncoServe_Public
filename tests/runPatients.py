import json
import requests
import unittest
import pdb
import os, shutil
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
import oncoserve.aggregators.basic as aggregators

DOMAIN = "http://localhost:5000"


START_DIR = '/home/yala/CD_dicoms'
PATIENTS = ['MiljaPoe' ,'ReginaCook','RichelleNessralla']
self.MRN = '1111111'
self.ACCESSION = '1111111'
self.METADATA = {'mrn':self.MRN, 'accession': self.ACCESSION}

def get_dicoms(dir_path):
    dicom_paths = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            dicom_paths.append( os.path.joint(root, filename) )
    return [open(path,'rb') for path in dicom_paths]

def get_patient_score(patient_dir):
    dir_path = os.path.joing(START_DIR, patient_dir)

    dicoms= [('dicom',file) for file in get_dicoms(dir_path)]

    '''
     1. Load dicoms. Make sure to filter by view, MIT app will not take responsibility for this.
    '''

    dicoms = [('dicom',self.f1), ('dicom',self.f2), ('dicom',self.f3), ('dicom', self.f4)]

    '''
    2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
    Note, files should contain a list of tuples:
     [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
    Deviating from this may result in unexpected behavior.
    '''
    r = requests.post(os.path.join(DOMAIN,"serve"), files=dicoms,
                      data=self.METADATA)
    '''
    3. Results will contain prediction, status, version info, all original metadata
    '''
    print(r.__dict__)
    self.assertEqual(r.status_code, 200)
    content = json.loads(r.content)
    pdb.set_trace()

for patient in PATIENTS:
    get_patient_score(patient)
