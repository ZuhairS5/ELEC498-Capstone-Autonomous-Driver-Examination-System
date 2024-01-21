import argparse
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import torch.optim.adam
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
from model import model


def train(n_epochs, optimizer, model, loss_fn, train_loader, val_loader, scheduler, device, plot_file, save_file):
    print('training...')
    model.train()
    losses_train = []
    losses_val = []

    for epoch in range(1, n_epochs + 1):
        print('epoch', epoch)
        loss_train = 0.0
        loss_val = 0.0

        for phase, loader in [('train', train_loader), ('val', val_loader)]:
            for imgs, labels in loader:
                imgs = imgs.view(imgs.size(0), -1).to(device=device)  # Flatten input images

                if phase == 'val':
                    model.eval()
                    with torch.no_grad():
                        outputs = model(imgs)
                        loss = loss_fn(outputs, imgs)
                        loss_val += loss.item()
                # train phase
                else:
                    model.train()
                    outputs = model(imgs)
                    loss = loss_fn(outputs, imgs)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    loss_train += loss.item()

            scheduler.step(loss_train)

        losses_train += [loss_train / len(train_loader)]
        losses_val += [loss_val / len(val_loader)]

        print('{} Epoch {}, Training loss {}, Validation loss {}'.format(
            datetime.now(), epoch, loss_train / len(train_loader), loss_val / len(val_loader)))

    if plot_file is not None:
        plt.figure(2, figsize=(12, 7))
        plt.clf()
        plt.plot(losses_train, label='train')
        plt.plot(losses_val, label='val')
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.legend(loc=1)
        plt.savefig(plot_file)

    if save_file:
        torch.save(my_model.state_dict(), save_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training Function')
    parser.add_argument('-z', type=int, default=8, help='Bottleneck size (default: 8)')
    parser.add_argument('-e', type=int, default=10, help='Number of epochs (default: 10)')
    parser.add_argument('-b', type=int, default=1024, help='Batch size (default: 1024)')
    parser.add_argument('-s', type=str, default="MLP.8.pth",
                        help='PyTorch model state save location name (default: "MLP.8.pth")')
    parser.add_argument('-p', type=str, default="loss.MLP.8.png",
                        help='PyTorch loss graph save location name (default: "loss.MLP.8.png")')

    arguments = parser.parse_args()

    # train_transform = transforms.Compose([transforms.ToTensor()])
    # train_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])  # EX
    train_transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(0, 1)])

    train_set = MNIST('./data/mnist', train=True, download=True, transform=train_transform)

    train_subset, val_subset = torch.utils.data.random_split(train_set, [50000, 10000],
                                                             generator=torch.Generator().manual_seed(1))
    # Splitting the training set into train and validation subsets

    train_data = DataLoader(train_subset, batch_size=arguments.b, shuffle=True)
    val_data = DataLoader(val_subset, batch_size=(int(arguments.b/4)), shuffle=True)  # Val set batch is 25% of train

    my_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    my_model = model(N_bottleneck=arguments.z)

    my_optimizer = torch.optim.Adam(my_model.parameters(), lr=1e-3, weight_decay=1e-5)

    my_loss_fn = torch.nn.MSELoss()

    my_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(my_optimizer)

    train(n_epochs=arguments.e, optimizer=my_optimizer, model=my_model, loss_fn=my_loss_fn,
          train_loader=train_data, val_loader=val_data, scheduler=my_scheduler,
          device=my_device, plot_file=arguments.p, save_file=arguments.s)
