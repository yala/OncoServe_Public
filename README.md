# OncoServe

## Big Picture
This repo is a wrapper of OncoNet (yala/OncoNet) and OncoData
(swansonk/OncoData) and supports the rolling out of OncoNet models
into production environments.

- OncoData handles conversion from dicom to png
- OncoNet research repo that
- OncoServe should wrap the model in a server that allows it to return outputs in real time.

## How to run it?
Docker image for most recent version is at:

yala/oncoserve:0.1.1


The docker container takes the following environment variables:
- LOGFILE: Where to write info+error logs to.
- CONFIG_NAME: Which app configuration to use. config.DensityConf is the
density application. config.CancerDetectionConfig is the risk application.
- TMP_IMG_DIR: Where to store temporary files

You can run the density app with the following command:

```docker run -p 5000:5000 -e LOGFILE=LOGS -e CONFIG_NAME=config.DensityConfig -e TMP_IMG_DIR=/OncoServe/tmp_images  -v ~/OncoServe/LOGS:/OncoServe/LOGS  -v ~/OncoServe/tmp_images:/OncoServe/tmp_images yala/oncoserve:0.1.1```

## How to use it?
See `tests/testClient.py` for a usage example in python.

Server will on: domain.partners.org:5000/serve.

