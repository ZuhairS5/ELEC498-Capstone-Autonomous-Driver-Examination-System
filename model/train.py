import argparse
from datetime import datetime
from os import truncate
import matplotlib.pyplot as plt
from torch import _functional_assert_async
import torch.optim.adam
from torch.utils.data import DataLoader
from model import model
import data_set
import csv
from torchsummary import summary

train_path = 'v1.0-traindataset.csv'
def train(n_epochs, optimizer, model, loss_fn, train_loader, scheduler, device, save_file, yolo):
    print("begining train loop")
    model.train()
    losses_train = []
    losses_val = []

    for epoch in range(1, n_epochs + 1):
        print('epoch', epoch)
        loss_train = 0.0
        loss_val = 0.0
        i=0
        model.train()
        for imgs, labels in train_loader:
            i+=1
            yolo = yolo.to(my_device)
            imgs = imgs.to(my_device)
            print(f"batch #{i} of {len(train_loader)}")
            y_outs = yolo(imgs)[0]
            # train phase
            y_outs = y_outs.to(my_device)
            labels = labels.to(my_device)
            outputs = model(y_outs)
            if i %100 ==0:
              print(labels)
              print(outputs)
              print(loss_train)
            labels = torch.flatten(labels, 1)
            loss = loss_fn(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            loss_train += loss.item()

        scheduler.step(loss_train)

        losses_train += [loss_train / len(train_loader)]
        #losses_val += [loss_val / len(val_loader)]
        torch.save(my_model.state_dict(), save_file)
       # print('{} Epoch {}, Training loss {}, Validation loss {}'.format(
       #     datetime.now(), epoch, loss_train / len(train_loader), loss_val / len(val_loader)))

        print('{} Epoch {}, Training loss {}'.format(datetime.now(), epoch, loss_train / len(train_loader)))
    plt.plot(losses_train)
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.savefig("loss")
   # if plot_file is not None:
   #     plt.figure(2, figsize=(12, 7))
   #     plt.clf()
   #     plt.plot(losses_train, label='train')
   #     plt.plot(losses_val, label='val')
   #     plt.xlabel('epoch')
   #     plt.ylabel('loss')
   #     plt.legend(loc=1)
   #     plt.savefig(plot_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Training Function')
    parser.add_argument('-validate', type=bool, default=True, help="Run validation steps")
    parser.add_argument('-e', type=int, default=10, help='Number of epochs (default: 10)')
    parser.add_argument('-b', type=int, default=4, help='Batch size (default: 1024)')
    parser.add_argument('-s', type=str, default="capstone_model.pth",
                        help='PyTorch model state save location name (default: "capstone_model.pth")')
    parser.add_argument('-p', type=str, default="capstone_loss.png",
                        help='PyTorch loss graph save location name (default: "capstone_loss.png")')
    arguments = parser.parse_args()

    objects = []
    with open(train_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None) #skip headers
        for row in csv_reader:
            object = {"filename": row[0], "label": row[2]}
            if object["label"] == "True":
                object["label"] = torch.Tensor([0,1])
            else:
                object["label"] = torch.Tensor([1, 0])
            objects.append(object)
    dataset = data_set.dataset(objects, "./data/")

    #train_subset, val_subset = torch.utils.data.random_split(dataset, [50000, 10000],
    #                                                         generator=torch.Generator().manual_seed(1))
    # Splitting the training set into train and validation subsets

    train_data = DataLoader(dataset, batch_size=arguments.b, shuffle=True)


    my_device = torch.device("cuda")

    my_model = model()
    my_yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True, classes=1)
    my_model.to(my_device)

    my_optimizer = torch.optim.Adam(my_model.parameters(), lr=1e-4)

    my_loss_fn = torch.nn.BCELoss()


    my_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(my_optimizer, patience = 2, threshold = 1e-2)
    train(n_epochs=arguments.e, optimizer=my_optimizer, model=my_model, loss_fn=my_loss_fn,
      train_loader=train_data, scheduler=my_scheduler,
      device=my_device, save_file=arguments.s, yolo = my_yolo)
