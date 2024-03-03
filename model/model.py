
import torch
from torch import nn
import torchvision

class model (nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.resNext = torchvision.models.resnet50(weights = None)
        self.fc1 = nn.Linear(1000,100)
        self.fc2= nn.Linear(100, 10)
        self.fc3 = nn.Linear(10,2)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)
        # = torch.hub.load('pytorch/vision:v0.10.0', 'resnext50_32x4d', pretrained=True)

    def forward(self, x):
        x = self.resNext(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.sig(x)
        x = self.softmax(x)
        return x