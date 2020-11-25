# OncoServe: Deploying Deep Learning Models for Breast Cancer Risk

## Introduction
This repository shares the models described in [A Deep Learning Mammography-Based Model for Improved Breast Cancer Risk Prediction](https://pubs.rsna.org/doi/), [A Deep Learning Model to Triage Screening Mammograms: A Simulation Study
](https://pubs.rsna.org/doi/10.1148/radiol.2019182908) and [Mammographic Breast Density Assessment Using
Deep Learning: Clinical Implementation](https://pubs.rsna.org/doi/10.1148/radiol.2018180694) as a (Flask) webserver.  You can send the webserver regular HTTP requests with a list of dicoms for a given mammogram, and a set of metadata keys (like MRN or Accession), and the webserver will return the DL density assessment along back with the same metadata. We note that we do not support all dicom formats, we assume presentation view mammograms, and have only tested this system with Hologic mammograms.

## Usage
This tool is provided for research purposes only and no responsibility is accepted for clinical decisions arising from its use. It is available upon request (email adamyala@mit.edu).  Commercial use requires a license, for further information please email adamyala@mit.edu.

## Structure:
OncoServe spins up a webserver in a docker container encapsulating all the software requirments to convert dicoms, and run the deep learning models. It imports [OncoNet](https://github.com/yala/OncoNet_Public) and [OncoData](https://github.com/yala/OncoData_Public) as submodules.

The repositories perform the following functions:
- [OncoData](https://github.com/yala/OncoData_Public): handles conversion from dicom to png
- [OncoNet](https://github.com/yala/OncoNet_Public): used for model development and training.
- [OncoServe](https://github.com/yala/OncoServe_Public): Wraps model in a webserver that allows it to return outputs in real time given an HTTP request. Used in clinical implementations. 

## System Requirements
- [Docker](https://www.docker.com/)
- 32 GB of RAM, 32GB of Disk.

## How to run it?
### Startup Steps:
- First, reach out directly to gain access. Please email adamyala@mit.edu with a brief
description of the study you intend to run.  Attach your dockerhub id.

- Next, we grant you access to the dockerhub image and indicate to you which image to pull from. 

- Pull most recent docker image from dockerhub.
``` docker pull learn2cure/name_of_docker_repo:0.1.0```

- Start the docker container following the instructions for the specific application (listed bellow).

### Running the Density Application:
```docker run -p 5000:5000 -e CONFIG_NAME=config.DensityConfig -v  /path/to/local/logfile:/OncoServe/LOGS:z  learn2cure/oncoserve_density:0.1.0```


### Running the Triage Application:
```docker run -p 5000:5000 -e CONFIG_NAME=config.MammoCancer1YrRiskImgOnlyConfig -v  /path/to/local/logfile:/OncoServe/LOGS:z  learn2cure/oncoserve_triage:0.1.0```

### Running the Image-Only DL 5-Year Risk Application
```docker run -p 5000:5000 -e CONFIG_NAME=config.MammoCancer5YrRiskImgOnlyConfig -v  /path/to/local/logfile:/OncoServe/LOGS:z  learn2cure/oncoserve_mammo_risk:0.1.1```
### Running the Hybrid DL 5-Year Risk Application: 
```docker run -p 5000:5000 -e CONFIG_NAME=config.MammoCancer5YrRiskHybridConfig -v  /path/to/local/logfile:/OncoServe/LOGS:z  learn2cure/oncoserve_mammo_risk:0.1.1```

### Notes on Docker 
The docker container takes the following environment variables:

- CONFIG_NAME: Which app configuration to use. config.DensityConf is the
density application. config.MammoCancer5YrRiskImgOnlyConfig is the risk application. The full list of configs is in `configs.py`
- DEVICE: Set DEVICE=GPU in order to use a GPU for model computation. Note, the examples above are for CPU only. To run OncoServe with a gpu, just add the the string `-e DEVICE=GPU` at the end of the command. It will run much faster. 

It will write to the following locations:
`/OncoServe/LOGS`: For all request level logs
`/OncoServe/tmp_images`: For temporary storage of images during processing

To view the logs/tmp images, you can mount those directories to outside the docker contained using `-v SOURCE_PATH:TARGER_PATH`  convention. The examples of running the apps is done with convention.

## How to use it?

### Streaming mode (One mammogram at a time):
Once your webserver is setup, you can get model assessments by sending it HTTP requests. 
See `tests/demo.py` for a usage example in python or `tests/demo.js` for a usage example in javascript. The demo is organized as a python test case, and show cases how the system should behave given faulty inputs and correct inputs. Note, you'll need to update the paths in the setUp function in the demo to refer to real dicom paths (see comments in the file).

### Batch mode:
This functionality is not yet supported; if you're interested in this functionality, please reachout to let me know. In the meanwhile, you can simple iterate through mammograms and HTTP request per mammogram. 

## Have questions?
Please email adamyala@mit.edu or post a github issue.
