import io
import requests
from PIL import Image
from torchvision import transforms
import torchvision.models as models
from torch.autograd import Variable


LABELS_URL = 'https://s3.amazonaws.com/outcome-blog/imagenet/labels.json'
IMG_URL = 'https://s3.amazonaws.com/outcome-blog/wp-content/uploads/2017/02/25192225/cat.jpg'

def analyzer(data, model):
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

    try:
        m = eval("models." + model + "(pretrained=True)")

        # Data normalization for validation
        data_transforms = transforms.Compose([
                            transforms.Scale(256),
                            transforms.CenterCrop(224),
                            transforms.ToTensor(),
                            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                        ])

        img_pil = Image.open(data)

        img_tensor = data_transforms(img_pil)
        img_tensor.unsqueeze_(0)

        # use_gpu = torch.cuda.is_available()

        img_variable = Variable(img_tensor)
        fc_out = m(img_variable)

        labels = {int(key):value for (key, value)
                  in requests.get(LABELS_URL).json().items()}

        output = labels[fc_out.data.numpy().argmax()]
        return {"output": output, "filenames": [data.filename]}
    except Exception as e:
        return {"error": str(e)}
