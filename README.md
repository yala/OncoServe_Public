# OncoServe: Deploying Deep Learning Models for Breast Cancer Risk Assessment, and Breast Density Assessment.

## Introduction
This repository shares the models described in [Towards Robust Mammography-Based Models for Breast Cancer Risk](https://www.science.org/doi/10.1126/scitranslmed.aba4373) and [Mammographic Breast Density Assessment Using
Deep Learning: Clinical Implementation](https://pubs.rsna.org/doi/10.1148/radiol.2018180694) as a (Flask) webserver.  You can send the webserver regular HTTP requests with a list of dicoms for a given mammogram, and a set of metadata keys (like MRN or Accession), and the webserver will return the model predictions along back with the same metadata. We note that we do not support all dicom formats, we assume presentation view mammograms, and have only tested this system with Hologic mammograms.

## Structure:
OncoServe spins up a webserver in a docker container encapsulating all the software requirments to convert dicoms, and run the deep learning models. It imports [Mirai](https://github.com/yala/Mirai) (and [OncoNet](https://github.com/yala/OncoNet_Public) for older models) and [OncoData](https://github.com/yala/OncoData_Public) as submodules.

The repositories perform the following functions:
- [OncoData](https://github.com/yala/OncoData_Public): handles conversion from dicom to png
- [Mirai](https://github.com/yala/Mirai) and [OncoNet](https://github.com/yala/OncoNet_Public) : used for model development and training.
- [OncoServe](https://github.com/yala/OncoServe_Public): Wraps model in a webserver that allows it to return outputs in real time given an HTTP request. Used in clinical implementations.

## System Requirements
- [Docker](https://www.docker.com/)
- 32 GB of RAM, 32GB of Disk.

## How to run it?
### Startup Steps:
- First, get the correct docker image from the research team. Due changes in legal guidance, this step now requires a collaboration agreement.

- Pull load the docker image from dockerhub.
``` docker load < filename.tar```

- Start the docker container following the instructions for the specific application (listed bellow).

### Running the Density Application:
```docker run -p 5000:5000 --shm-size 32G -e CONFIG_NAME=config.DensityConfig learn2cure/oncoserve_density:0.1.0```


### Running the Mirai Application:
```docker run -p 5000:5000 --shm-size 32G learn2cure/oncoserve_mirai:0.5.0```

## How to use it?

### Streaming mode (One mammogram at a time):
Once your webserver is setup, you can get model assessments by sending it HTTP requests.
See `tests/demo.py` for a usage example in python or `tests/demo.js` for a usage example in javascript. The python demo is organized as a python test case. Note, you'll need to update the paths in the setUp function in the demo to refer to real dicom paths (see comments in the file).

### Batch mode:
See the [Mirai](https://github.com/yala/Mirai) github. This will require logging into the docker container with a shell and running our batch processing scripts.

Note, batch processing is not supported under the density application.

## Have questions?
Please email adamyala@mit.edu.

## Usage
This tool and all associated code is provided for under MIT License.
