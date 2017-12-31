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
        'img_mean': 0.116562376848,
        'img_std': 0.192259717494,
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

