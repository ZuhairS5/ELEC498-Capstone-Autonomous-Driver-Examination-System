import torch
import os
from torch.utils.data import Dataset, DataLoader
import torchvision
from PIL import Image
from torchvision import transforms


def image_to_tensor(image_path):
    transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((1200, 1200))
    ])
    img = Image.open(image_path)
    convert_tensor = transforms.ToTensor()
    tensor = transform(convert_tensor(img))
    return tensor


class dataset(Dataset):
    def __init__(self, objects, root_dir):
        self.objects = objects
        self.root_dir = root_dir

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.objects[idx]["filename"])
        image = image_to_tensor(img_name)
        labels = self.objects[idx]["label"]
        sample = [image, labels]

        return sample
