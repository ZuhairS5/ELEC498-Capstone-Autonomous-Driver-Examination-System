import torch
from torchvision import transforms
from PIL import Image
import data_helpers

import csv
def image_to_tensor(image_path):
    img = Image.open(image_path)
    convert_tensor = transforms.ToTensor()
    tensor = torch.resize(torch.flatten(convert_tensor(img), 1),1000)
    return tensor

if __name__ == "__main__":
    with open('dataset.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None) #skip headers
        for row in csv_reader:
            tensor = image_to_tensor(row[0])
            print(tensor)