
import torch
from torch import nn

class input_parser(nn.Module):
    def __init__(self):
        super(input_parser, self).__init__()


    def forward(self, input):
        x = torch.flatten(input, start_dim=1)
        return x

class model (nn.Module):
    def __init__(self):
        super(model, self).__init__()
        self.parser = input_parser()
        self.resNext = torch.hub.load('pytorch/vision:v0.10.0', 'resnext50_32x4d', pretrained=True)

    def forward(self, x):
        x = self.input_parser(x)
        x = self.resNext(x)
        return x