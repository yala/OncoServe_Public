import logging
import torch
import torch.autograd as autograd
import torch.nn.functional as F
import numpy as np
import oncoserve.logger
import onconet.utils.parsing as parsing
from  onconet.transformers.basic import ComposeTrans
import  onconet.transformers.factory as transformer_factory
import oncoserve.aggregators.factory as aggregator_factory
import pdb

INIT_MESSAGE = "OncoNet- Initializing OncoNet Wrapper..."
TRANSF_MESSAGE = "OncoNet- Transfomers succesfully composed"
MODEL_MESSAGE = "OncoNet- Model successfully loaded from : {}"
AGGREGATOR_MESSAGE = "OncoNet- Aggregator [{}] succesfully loaded"
IMG_START_CLASSIF_MESSAGE = "OncoNet- Image classification start with tensor size {}"
IMG_FINISH_CLASSIF_MESSAGE = "OncoNet- Image classification produced {}"
EXAM_CLASSIF_MESSAGE = "OncoNet- Exam classification complete!"
ERR_MSG = "OncoNet- Fail to label exam. Exception: {}"

class OncoNetWrapper(object):
    def __init__(self, args, aggregator_name, logger):
        logger.info(INIT_MESSAGE)
        self.args = args
        args.cuda = args.cuda and torch.cuda.is_available()
        args.test_image_transformers = parsing.parse_transformers(args.test_image_transformers)
        args.test_tensor_transformers = parsing.parse_transformers(args.test_tensor_transformers)
        test_transformers = transformer_factory.get_transformers(
            args.test_image_transformers, args.test_tensor_transformers, args)


        self.transformer = ComposeTrans(test_transformers)
        logger.info(TRANSF_MESSAGE)
        self.model = torch.load(args.snapshot)
        logger.info(MODEL_MESSAGE.format(args.snapshot))
        self.aggregator = aggregator_factory.get_exam_aggregator(aggregator_name)

        self.logger = logger


    def process_image(self, image, risk_factor_vector=None):
        try:
            ## Apply transformers
            x = self.transformer(image, self.args.additional)
            x = autograd.Variable(x.unsqueeze(0))
            risk_factors = autograd.Variable(risk_factor_vector.unsqueeze(0)) if risk_factor_vector is not None else None
            self.logger.info(IMG_START_CLASSIF_MESSAGE.format(x.size()))
            if self.args.cuda:
                x = x.cuda()
                self.model = self.model.cuda()
            else:
                self.model = self.model.cpu()
            ## Index 0 to toss batch dimension
            pred_y = F.softmax(self.model(x, risk_factors)[0])[0]
            pred_y = self.args.label_map( pred_y.cpu().data.numpy() )
            self.logger.info(IMG_FINISH_CLASSIF_MESSAGE.format(pred_y))
            return pred_y
        except Exception as e:
            err_msg = ERR_MSG.format(e)
            raise Exception(err_msg)

    def process_exam(self, images, risk_factor_vector):
        preds = []
        for im in images:
            preds.append(self.process_image(im, risk_factor_vector))
        y = self.aggregator(preds)
        if isinstance(y, np.generic):
            y = y.item()
        self.logger.info(EXAM_CLASSIF_MESSAGE)
        return y
