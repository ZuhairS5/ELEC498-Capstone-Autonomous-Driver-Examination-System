import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import torch.optim.adam
from torch.utils.data import DataLoader
from model import model
import data_set
import csv

test_path = 'v1.0-testdataset.csv'

def test(test_loader, model, loss_fn):
    losses_test = []
    for images, labels in test_loader:
        loss_test = 0.0
        output = model(images)
        loss = loss_fn(output, labels)
        loss_test += loss.item
        losses_test += [loss_test/len(test_loader)]
    plt.plot(losses_test)
    plt.xlabel('batch')
    plt.ylabel('loss')
    plt.savefig("loss_test")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Training Function')
    parser.add_argument('-b', type=int, default=1024, help='Batch size (default: 1024)')
    parser.add_argument('-s', type =str, default = 'capstone_model.pth')
    arguments = parser.parse_args()

    objects = []
    with open(test_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # skip headers
        for row in csv_reader:
            object = {"filename": row[0], "label": row[2]}
            if object["label"]:
                object["label"] = torch.Tensor([0, 1])
            else:
                object["label"] = torch.Tensor([1, 0])
            objects.append(object)

    dataset = data_set.dataset(objects, "./data/")
    test_data = DataLoader(dataset, batch_size=arguments.b, shuffle=True)
    my_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    my_model = model()
    my_model.load_state_dict(torch.load(arguments.s))
    my_model.eval()
    my_loss_fn = torch.nn.BCELoss()
    test(test_data, my_model, my_loss_fn)