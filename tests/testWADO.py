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

## Example of WADO Failing
obj_uid_response = requests.post(OBJ_ENDPOINT , params={'accession':ACCESSION, 'mrn':MRN})

print(r.__dict__)
