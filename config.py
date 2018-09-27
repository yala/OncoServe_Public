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
    ONCOSERVE_VERSION = '0.2.0'
    ONCODATA_VERSION = '0.2.0'
    ONCONET_VERSION =  '0.2.0'
    ONCOQUERIES_VERSION =  '0.2.0'
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
        'img_mean': [7662.53827604],
        'img_std': [12604.0682836],
        'img_size': [256,256],
        'num_chan': 3,
        'num_gpus': 1,
        'test_image_transformers': ['scale_2d'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        'snapshot': 'snapshots/mgh_mammo_density_sep26_2018.pt',
        'label_map': density_label_func,
        'video':False,
        'use_precomputed_hiddens': False,
        'use_risk_factors':False,
        'callibrator_path': None
    }


    ONCONET_ARGS = Args(ONCONET_CONFIG)

class MammoCancer1YrDetectionConfig(Config):
    NAME = '2D_Mammo_Cancer_1Year_Detection'
    AGGREGATION="max"

    def cancer_risk_func(pred):
        return pred[1]

    ONCONET_CONFIG = {
        'cuda': False,
        'img_mean': [7240.058],
        'img_std': [12072.904],
        'img_size': [1664,2048],
        'num_chan': 3,
        'num_gpus': 1,
        'test_image_transformers': ['scale_2d', 'align_to_left'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        'label_map': cancer_risk_func,
        'snapshot': 'snapshots/mgh_mammo_cancer_1yr_detection_sep02_2018.pt',
        'video':False,
        'use_precomputed_hiddens': False,
        'use_risk_factors': True,
        'risk_factor_keys': "density binary_family_history binary_biopsy_benign binary_biopsy_LCIS binary_biopsy_atypical_hyperplasia age menarche_age menopause_age first_pregnancy_age prior_hist race parous menopausal_status weight height ovarian_cancer ovarian_cancer_age ashkenazi brca mom_bc_cancer_history m_aunt_bc_cancer_history p_aunt_bc_cancer_history m_grandmother_bc_cancer_history p_grantmother_bc_cancer_history sister_bc_cancer_history mom_oc_cancer_history m_aunt_oc_cancer_history p_aunt_oc_cancer_history m_grandmother_oc_cancer_history p_grantmother_oc_cancer_history sister_oc_cancer_history hrt_type hrt_duration hrt_years_ago_stopped",
        'use_region_annotation': False,
        'use_second_order_risk_factor_features': False,
        'callibrator_path': 'snapshots/callibrator_mgh_mammo_cancer_1yr_detection_sep19_2018.pt'
    }
    ONCONET_CONFIG['risk_factor_keys'] = ONCONET_CONFIG['risk_factor_keys'].split()
    ONCONET_ARGS = Args(ONCONET_CONFIG)

class MammoCancer5YrRiskConfig(Config):
    NAME = '2D_Mammo_Cancer_5Year_Risk'
    AGGREGATION="max"

    def cancer_risk_func(pred):
        return pred[1]

    ONCONET_CONFIG = {
        'cuda': False,
        'img_mean': [7240.058],
        'img_std': [12072.904],
        'img_size': [1664,2048],
        'num_chan': 3,
        'num_gpus': 1,
        'test_image_transformers': ['scale_2d', 'align_to_left'],
        'test_tensor_transformers': ["force_num_chan_2d", "normalize_2d"],
        'additional': None,
        'label_map': cancer_risk_func,
        'snapshot': 'snapshots/mgh_mammo_cancer_5yr_detection_hybrid_aug08_2018.pt',
        'video':False,
        'use_precomputed_hiddens': False,
        'use_risk_factors': True,
        'risk_factor_keys': "density binary_family_history binary_biopsy_benign binary_biopsy_LCIS binary_biopsy_atypical_hyperplasia age menarche_age menopause_age first_pregnancy_age prior_hist race parous menopausal_status weight height ovarian_cancer ovarian_cancer_age ashkenazi brca mom_bc_cancer_history m_aunt_bc_cancer_history p_aunt_bc_cancer_history m_grandmother_bc_cancer_history p_grantmother_bc_cancer_history sister_bc_cancer_history mom_oc_cancer_history m_aunt_oc_cancer_history p_aunt_oc_cancer_history m_grandmother_oc_cancer_history p_grantmother_oc_cancer_history sister_oc_cancer_history hrt_type hrt_duration hrt_years_ago_stopped",
        "use_region_annotation": False,
        'use_second_order_risk_factor_features': False,
        'callibrator_path': 'snapshots/callibrator_mgh_mammo_cancer_5yr_detection_hybrid_aug08_2018.pt'
    }
    ONCONET_CONFIG['risk_factor_keys'] = ONCONET_CONFIG['risk_factor_keys'].split()
    ONCONET_ARGS = Args(ONCONET_CONFIG)
    ONCONET_ARGS = Args(ONCONET_CONFIG)
