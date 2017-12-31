import logging
import torch
import torch.autograd as autograd
import oncoserve.logger
import onconet.utils.parsing as parsing
from  onconet.transformers.basic import ComposeTrans
import  onconet.transformers.factory as transformer_factory
import oncoserve.aggregators.factory as aggregator_factory
import pdb

logger = oncoserve.logger.get_logger('oncologger.onconet', 'errors.log')

INIT_MESSAGE = "Initializing OncoNet Wrapper..."
TRANSF_MESSAGE = "Transfomers succesfully composed"
MODEL_MESSAGE = "Model successfully loaded from : {}"
AGGREGATOR_MESSAGE = "Aggregator [{}] succesfully loaded"
IMG_CLASSIF_MESSAGE = "Image classification produced {}"
EXAM_CLASSIF_MESSAGE = "Exam classification complete!"


class OncoNetWrapper(object):
    def __init__(self, args, aggregator_name):
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
        logger.info(AGGREGATOR_MESSAGE.format(aggregator_name))


    def process_image(self, image):
        ## Apply transformers
        x = self.transformer(image, self.args.additional)
        logger.info("Ran image through transforms")
        x = x.unsqueeze(0)
        logger.info("Unsqueeze image into batch shape")
        pdb.set_trace()
        x = autograd.Variable(x)
        if self.args.cuda:
            x = x.cuda()
        pred_y = self.model(x)
        logger.info("get pred")
        #Find max pred
        pdb.set_trace()
        pred_y = self.args.label_map[ pred_y.data.numpy().argmax() ]
        logger.info(IMG_CLASSIF_MESSAGE.format(pred_y))
        return pred_y

    def process_exam(self, images):
        preds = []
        for im in images:
            preds.append(self.process_image(im))
        y = self.aggregator(preds)
        logger.info(EXAM_CLASSIF_MESSAGE)
        return y
