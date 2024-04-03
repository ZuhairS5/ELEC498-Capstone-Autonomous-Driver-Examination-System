import torch
from torch import nn
import torchvision
import pandas as pd

class model (nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=False, classes = 1)
        self.fc1 = nn.Linear(115200,10)
        self.fc2 = nn.Linear(10, 2)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)
        # = torch.hub.load('pytorch/vision:v0.10.0', 'resnext50_32x4d', pretrained=True)

    def forward(self, x):
        x = self.yolo(x)
        print("Yolo Out")
        print(len(x))
        for y in range(len(x)):
            print(len(x[y]))
        print(x[0].shape)
        print(x[1].shape)
        print(x[2].shape)
        print("-------------")
        #print(x[0])
        #print(x[1])
        x = torch.flatten(x[0], 1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sig(x)
        x = self.softmax(x)
        return x
