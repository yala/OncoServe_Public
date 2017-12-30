import logging
import torch
import OncoNet.onconet.utils.parsing as parsing
from  OncoNet.onconet.transformers.basic import ComposeTrans
import  OncoNet.onconet.transformers.transformer_factory as transformer_factory
import aggregators.factory as aggregator_factory
logger = logging.getLogger('oncologger.onconet')


class OncoNetWrapper(object):
    def __init__(self, args):
        logger.info("Initializing OncoNet Wrapper...")
        self.args = args
        args.cuda = args.cuda and torch.cuda.is_available()
        args.test_image_transformers = parsing.parse_transformers(args.test_image_transformers)
        args.test_tensor_transformers = parsing.parse_transformers(args.test_tensor_transformers)
        test_transformers = transformer_factory.get_transformers(
            args.test_image_transformers, args.test_tensor_transformers, args)


        self.transformer = ComposeTrans(test_transformers)
        logger.info("Transfomers succesfully composed")
        self.model = torch.load(args.snapshot)
        logger.info("Model successfully loaded from : {}".format(args.snapshot))
        self.aggregator = aggregator_factory(args)
        logger.info("Aggregator [{}] succesfully loaded".format(args.aggregator))



    def process_image(self, image):
        ## Apply transformers
        x = self.transformer(image, self.args.additional)

        x = x.unsqueeze(0)
        pred_y = self.model(x)
        #Find max pred
        pred_y = self.args.label_map[ pred_y.data.numpy().argmax() ]
        logger.info("Image classification complete!")
        return pred_y

    def process_exam(self, images):
        preds = []
        for im in images:
            preds.append(self.process_image(im))
        y = self.aggregator(preds)
        logger.info("Exam classification complete!")
        return y