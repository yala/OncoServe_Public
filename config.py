import os

class Args(object):
    def __init__(self, config_dict):
        self.__dict__.update(config_dict)

class Config(object):
    DEBUG=False
    AGGREGATION="none"
    ONCONET_CONFIG = {}
    ONCODATA_CONFIG = {
        'convertor': 'dcmtk',
        'temp_img_dir': os.environ['TMP_IMG_DIR']
    }
    ONCONET_ARGS = Args(ONCONET_CONFIG)
    ONCODATA_ARGS = Args(ONCODATA_CONFIG)
    ONCOSERVE_VERSION = '0.1.0'
    ONCODATA_VERSION = '0.1.0'
    ONCONET_VERSION =  '0.0.9'
    NAME = 'BaseConfig'
    PORT = 5000


class DensityConfig(Config):
    NAME = '2D_Mammo_Breast_Density'
    AGGREGATION="vote"
    ONCONET_CONFIG = {
        'cuda': False,
        'dropout': .1,
        'img_mean': 7662.53827604,
        'img_std': 12604.0682836,
        'img_size': [256,256],
        'num_chan': 3,
        'num_gpus': 1,
        'model_name': 'resnet18',
        'test_image_transformers': ['scale_2d'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        'snapshot': 'snapshots/best_4way.pt',
        'label_map': [1, 2, 3, 4],
        'make_fc': False
    }
    ONCONET_ARGS = Args(ONCONET_CONFIG)

class CancerDetectionConfig(Config):
    NAME = '2D_Mammo_Cancer_Detection'
    AGGREGATION="max"
    ONCONET_CONFIG = {
        'cuda': False,
        'dropout': .1,
        'img_mean': 7662.53827604,
        'img_std': 12604.0682836,
        'img_size': [256,256],
        'num_chan': 3,
        'num_gpus': 1,
        'test_image_transformers': ['scale_2d align_to_left'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        'snapshot': 'snapshots/cancer_v0.1.1.pt',
        'label_map': [1, 2, 3, 4],
        'make_fc': True
    }
    ONCONET_ARGS = Args(ONCONET_CONFIG)

