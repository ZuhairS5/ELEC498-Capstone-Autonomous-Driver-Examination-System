import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import torch.optim.adam
from torch.utils.data import DataLoader
from model import model
import data_set
import csv

train_path = 'v1.0-traindataset.csv'
def train(n_epochs, optimizer, model, loss_fn, train_loader, scheduler, device, save_file):
    print("begining train loop")
    model.train()
    losses_train = []
    losses_val = []

    for epoch in range(1, n_epochs + 1):
        print('epoch', epoch)
        loss_train = 0.0
        loss_val = 0.0
        for imgs, labels in train_loader:
            # train phase
            model.train()
            outputs = model(imgs)
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
    parser.add_argument('-b', type=int, default=1024, help='Batch size (default: 1024)')
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
            if object["label"]:
                object["label"] = torch.Tensor([0,1])
            else:
                object["label"] = torch.Tensor([1, 0])
            objects.append(object)
    dataset = data_set.dataset(objects, "./data/")

    #train_subset, val_subset = torch.utils.data.random_split(dataset, [50000, 10000],
    #                                                         generator=torch.Generator().manual_seed(1))
    # Splitting the training set into train and validation subsets

    train_data = DataLoader(dataset, batch_size=arguments.b, shuffle=True)


    my_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    my_model = model()

    my_optimizer = torch.optim.Adam(my_model.parameters(), lr=1e-4, weight_decay=1e-5)

    my_loss_fn = torch.nn.BCELoss()

    my_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(my_optimizer)
    train(n_epochs=arguments.e, optimizer=my_optimizer, model=my_model, loss_fn=my_loss_fn,
      train_loader=train_data, scheduler=my_scheduler,
      device=my_device, save_file=arguments.s)
