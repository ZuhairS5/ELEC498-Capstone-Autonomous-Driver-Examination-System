import torch
from torch import nn

class model (nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.fc1_3 = nn.Linear(38400, 1000)
        self.fc2 = nn.Linear(3000, 100)
        self.fc3 = nn.Linear(100, 2)
        self.relu = nn.ReLU()
        self.sig = nn.Sigmoid()
        self.softmax = nn.Softmax(dim=1)
        # = torch.hub.load('pytorch/vision:v0.10.0', 'resnext50_32x4d', pretrained=True)

    def forward(self, x):
        x = torch.flatten(x, 2)
        x = self.fc1_3(x)
        x = self.relu(x)
        x = torch.flatten(x, 1)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.sig(x)
        x = self.softmax(x)
        return x
