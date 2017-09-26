import io
import requests
import json
import logging
from PIL import Image
from torchvision import transforms
import torchvision.models as models
from torch.autograd import Variable


LABELS_URL = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'
logger = logging.getLogger('oncologger.learning')

def analyzer(data, model, aggregation):
    # d = {
    #     "alexnet": models.alexnet(pretrained=True),
    #     "resnet18": models.resnet18(pretrained=True),
    #     "resnet34": models.resnet34(pretrained=True),
    #     "resnet50": models.resnet50(pretrained=True),
    #     "resnet101": models.resnet101(pretrained=True),
    #     "resnet152": models.resnet152(pretrained=True),
    #     "squeezenet1.0": models.squeezenet1_0(pretrained=True),
    #     "squeezenet1.1": models.squeezenet1_1(pretrained=True),
    # }
    logger.info("Starting classification process...")
    try:
        outputs = []
        filenames = []

        m = eval("models." + model + "(pretrained=True)")
        logger.info("Model successfully loaded!")
        # Data normalization for validation
        data_transforms = transforms.Compose([
                            transforms.Scale(256),
                            transforms.CenterCrop(224),
                            transforms.ToTensor(),
                            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                        ])

        labels = {int(key):value for (key, value)
                    in requests.get(LABELS_URL).json().items()}

        x = 0
        for img in data:
            logger.info("Opening image " + str(x) + "...")
            img_pil = Image.open(img)

            logger.info("Transforming image...")
            img_tensor = data_transforms(img_pil)
            img_tensor.unsqueeze_(0)

            logger.info("Predicting result...")
            img_variable = Variable(img_tensor)
            fc_out = m(img_variable)

            outputs.append(labels[fc_out.data.numpy().argmax()])
            filenames.append(img.filename)
            x = x + 1
        logger.info("Image classification complete!")

        logger.info("Aggregating results...")
        if (aggregation == "first"):
            output = outputs[0]
        elif (aggregation == "last"):
            output = outputs[-1]
        elif (aggregation == "max"):
            output = max(set(outputs), key=outputs.count)
        elif (aggregation == "min"):
            output = min(set(outputs), key=outputs.count)
        elif (aggregation == "none"):
            output = '; '.join(outputs)

        logger.info("Results successfully aggregated!")
        return {"output": output, "filenames": filenames}
    except Exception as e:
        logging.error(str(e))
        return {"error": str(e)}
