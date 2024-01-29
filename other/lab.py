import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from torchvision.utils import make_grid
from torchinfo import summary
# from torchsummary import summary
import vector_quantize_pytorch as vq
# import torchtext
# from torch.utils.data.distributed import DistributedSampler
# import torch.distributed as dist
# import torch.multiprocessing as mp
# from torch.nn.parallel import DistributedDataParallel as DDP
from PIL import Image

SEED = 42
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
print('Device:', device)
# https://pytorch.org/docs/stable/hub.html
entrypoints = torch.hub.list('pytorch/vision', force_reload=True)
print(entrypoints)

from torchvision.models.detection import FasterRCNN, maskrcnn_resnet50_fpn, MaskRCNN_ResNet50_FPN_Weights
from torchvision.models.quantization import QuantizableMobileNetV3
from torchvision.models import resnet18, ResNet18_Weights, resnet34, ResNet34_Weights, resnet50, ResNet50_Weights, resnet101, ResNet101_Weights

# https://debuggercafe.com/train-pytorch-retinanet-on-custom-dataset/
# https://pytorch.org/vision/stable/models.html
# https://huggingface.co/docs


def test_classification():
    weights = ResNet101_Weights.DEFAULT
    # print(dir(weights))
    preprocess = weights.transforms()
    model = resnet101(weights=weights).to(device)  # pretrained=True is deprecated
    model.eval()

    data = torch.randn(1, 3, 256, 256).to(device)
    summary(model=model, 
            input_data=data, 
            verbose=1,
            col_names=["input_size", "output_size", "params_percent", "num_params", "trainable", "mult_adds",], 
            col_width=20)

    im = Image.open('../img/capibara.jpg')
    # im = im.resize((256, 256))
    print(im.size)
    im = preprocess(im).unsqueeze(0).to(device)
    print(im.shape)

    with torch.no_grad():
        out = model(im)
        class_id = out.argmax(dim=1).item()
        score = out[0, class_id].item()
        print('Class ID:', class_id)
        print('Predicted:', weights.meta["categories"][class_id])
        print('Score:', score)


def test_instance_segmentation():
    weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
    # print(dir(weights))
    preprocess = weights.transforms()
    model = maskrcnn_resnet50_fpn(weights=weights).to(device)  # pretrained=True is deprecated
    model.eval()

    data = torch.randn(1, 3, 256, 256).to(device)
    summary(model=model, 
            input_data=data, 
            verbose=1,
            col_names=["input_size", "output_size", "params_percent", "num_params", "trainable", "mult_adds",], 
            col_width=20)
    
if __name__ == "__main__":
    test_classification()
    # test_instance_segmentation()
