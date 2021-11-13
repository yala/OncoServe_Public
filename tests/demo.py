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

class Test_MIT_App(unittest.TestCase):

    def setUp(self):
        self.f1 = open("/home/yala/sample_dicoms/1.dcm", 'rb')
        self.f2 = open("/home/yala/sample_dicoms/2.dcm", 'rb')
        self.f3 = open("/home/yala/sample_dicoms/3.dcm", 'rb')
        self.f4 = open("/home/yala/sample_dicoms/4.dcm", 'rb')
        # Fake MRN
        self.MRN = '11111111'
        # Fake Accession
        self.ACCESSION = '2222222'
        self.METADATA = {'mrn':self.MRN, 'accession': self.ACCESSION}



    def tearDown(self):
        try:
            self.f1.close()
            self.f2.close()
            self.f3.close()
            self.f4.close()
        except Exception as e:
            pass

    def test_normal_request(self):
        '''
        Demo of how to use MIRAI. Note, this is applicable for all MIRAI applications.
        '''

        '''
         1. Load dicoms. Make sure to filter by view, MIRAI will not take responsibility for this.
        '''

        files = [('dicom',self.f1), ('dicom',self.f2), ('dicom',self.f3), ('dicom', self.f4)]

        '''
        2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
        Note, files should contain a list of tuples:
         [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
        Deviating from this may result in unexpected behavior.
        '''
        r = requests.post(os.path.join(DOMAIN,"serve"), files=files,
                          data=self.METADATA)
        '''
        3. Results will contain prediction, status, version info, all original metadata
        '''
        print(r.__dict__)
        self.assertEqual(r.status_code, 200)
        content = json.loads(r.content)
        self.assertEqual(content['metadata']['mrn'], self.MRN)
        self.assertEqual(content['metadata']['accession'], self.ACCESSION)

if __name__ == '__main__':
    unittest.main()
