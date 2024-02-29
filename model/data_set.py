import data_helpers
import torch
import os
from torch.utils.data import Dataset, DataLoader


class dataset(Dataset):
    def __init__(self, objects, root_dir, transform=None):
        """
        Arguments:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.objects = objects
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.objects[idx]["filename"])
        image = data_helpers.image_to_tensor(img_name)
        labels = self.objects[idx]["label"]
        sample = [image, labels]

        if self.transform:
            sample = self.transform(sample)

        return sample
