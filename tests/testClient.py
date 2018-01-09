import urllib2
import json
import requests
import unittest
import pdb
import os, shutil
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
import oncoserve.aggregators.basic as aggregators

class Test_MIT_App(unittest.TestCase):

    def setUp(self):
        self.f1 = open("/home/yala/sample_dicoms/1.dcm", 'rb')
        self.f2 = open("/home/yala/sample_dicoms/2.dcm", 'rb')
        self.f3 = open("/home/yala/sample_dicoms/3.dcm", 'rb')
        self.f4 = open("/home/yala/sample_dicoms/4.dcm", 'rb')
        self.bad_f = open("/home/yala/sample_dicoms/bad.txt", 'rb')
        self.MRN = '2553222'
        self.ACCESSION = '12117409'
        self.METADATA = {'mrn':self.MRN, 'accession': self.ACCESSION}

    def tearDown(self):
        self.f1.close()
        self.f2.close()
        self.f3.close()
        self.f4.close()
        self.bad_f.close()

    def test_normal_request(self):

        # Demo of how to use MIT APP

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
        r = requests.post("http://localhost:5000/serve", files=dicoms,
                          data=self.METADATA)
        '''
        3. Results will contain prediction, status, version info, all original metadata
        '''
        print(r.__dict__)
        self.assertEqual(r.status_code, 200)
        content = json.loads(r.content)
        self.assertEqual(content['prediction'], 3)
        self.assertEqual(content['metadata']['mrn'], self.MRN)
        self.assertEqual(content['metadata']['accession'], self.ACCESSION)

    def test_bad_dicom_request(self):

        # Example of failed request:
        '''
            1. Get faulty dicoms
        '''
        dicoms = [('dicom',self.f1), ('dicom', self.bad_f), ('dicom', self.f3), ('dicom', self.f4)]
        '''
            2. Send request to model at /serve with dicoms in files field, and any metadata in the data field
        '''
        r = requests.post("http://localhost:5000/serve", files=dicoms,
                          data=self.METADATA)
        '''
            3. Results will contain prediction == None, and an error code about
            which dicom couldn't convert
        '''
        print(r.__dict__)
        self.assertEqual(r.status_code, 500)
        content = json.loads(r.content)
        self.assertEqual(content['prediction'], None)
        self.assertEqual(content['metadata']['mrn'], self.MRN)
        self.assertEqual(content['metadata']['accession'], self.ACCESSION)

    def test_max_aggregator(self):

        examples = [ ([1,3,4,10,10.1], 10.1) ,
                     ([1], 1),
                     ([1,3,4,10,-10.1], 10.1) ]

        for preds, ans in examples:
            self.assertEqual(aggregators.aggregate_max(preds), ans)

    def test_vote_aggregator(self):
        examples = [ ([1,3,4, 1], 1) ,
                     ([1, 1, 1, 3, 3], 1),
                     ([5,5,5,5, 1], 5) ]

        for preds, ans in examples:
            self.assertEqual(aggregators.aggregate_vote(preds), ans)


if __name__ == '__main__':
    unittest.main()
