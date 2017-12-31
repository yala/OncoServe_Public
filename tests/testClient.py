import urllib2
import json
import requests

DOMAIN = "https://emimld01.partners.org/MLWadoProxyService/api/{}"
OBJ_ENDPOINT = DOMAIN.format("MLImagesGetDataAPI")
DICOM_ENDPOINT = DOMAIN.format("MLImagesGetDicomImageAPI")
PNG_ENDPOINT = DOMAIN.format("MLImagesGetPNGImageAPI")

MRN = '2553222'
ACCESSION = '12117409'
METADATA = {'mrn':MRN, 'accession': ACCESSION}


## Get UIDS

obj_uid_response = requests.post(OBJ_ENDPOINT , params={'accession':ACCESSION, 'mrn':MRN})

f1 = open("sample_dicoms/1.dcm", 'rb')
f2 = open("sample_dicoms/2.dcm", 'rb')
f3 = open("sample_dicoms/3.dcm", 'rb')
f4 = open("sample_dicoms/4.dcm", 'rb')

dicoms = [('dicom',f1), ('dicom',f2), ('dicom',f3), ('dicom',f4)]

r = requests.post("http://localhost:5000/serve", files=dicoms, data=METADATA)

print(r.__dict__)
