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
    ONCOSERVE_VERSION = '0.1.1'
    ONCODATA_VERSION = '0.1.0'
    ONCONET_VERSION =  '0.1.0'
    NAME = 'BaseConfig'
    PORT = 5000


class DensityConfig(Config):
    NAME = '2D_Mammo_Breast_Density'
    AGGREGATION="vote"

    def density_label_func(pred):
        pred = pred.argmax()
        density_labels = [1,2,3,4]
        return density_labels[pred]

    ONCONET_CONFIG = {
        'cuda': False,
        'dropout': .1,
        'img_mean': [7662.53827604],
        'img_std': [12604.0682836],
        'img_size': [256,256],
        'num_chan': 3,
        'num_gpus': 1,
        'model_name': 'resnet18',
        'test_image_transformers': ['scale_2d'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        'snapshot': 'snapshots/best_4way_py3.pt',
        'label_map': density_label_func,
        'video':False,
        'use_precomputed_hiddens': False,
        'use_risk_factors':False
    }


    ONCONET_ARGS = Args(ONCONET_CONFIG)

class CancerDetectionConfig(Config):
    NAME = '2D_Mammo_Cancer_Detection'
    AGGREGATION="max"

    def cancer_risk_func(pred):
        return pred[1]

    ONCONET_CONFIG = {
        'cuda': False,

        'dropout': .1,
        'img_mean': 7240.058,
        'img_std': 12072.904,
        'img_size': [1664,2048],
        'num_chan': 3,
        'num_gpus': 1,
        'test_image_transformers': ['scale_2d', 'align_to_left'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        "model_name": "aggregator",
        'snapshot': 'snapshots/cancer_v0.1.1.pt',
        'label_map': cancer_risk_func,
        'make_fc': True
    }
    ONCONET_ARGS = Args(ONCONET_CONFIG)

