import torch
from torch import nn
import torchvision

class model (nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=False, classes = 1)
        self.fc1 = nn.Linear(115200,10)
        self.fc2 = nn.Linear(10, 2)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=0)
        # = torch.hub.load('pytorch/vision:v0.10.0', 'resnext50_32x4d', pretrained=True)

    def forward(self, x):
        x = self.yolo(x)
        x = torch.flatten(x[0], 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sig(x)
        x = self.softmax(x)
        return x
