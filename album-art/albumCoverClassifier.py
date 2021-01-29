import numpy as np
import matplotlib.pyplot as plt

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from albumCovers import getInfo

# use gpu if available
dev = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
if not torch.cuda.is_available(): quit() # basically need to utilize gpu for my machine

class Network(nn.Module):
    def __init__(self, image_dims=640, max_pool_size=2, stride=2, filter_size=5, layer1_out_channels=8, layer2_out_channels=12, layer1_padding=0, layer2_padding=2):
        super().__init__()
        self.layer1_padding = layer1_padding
        self.layer2_padding = layer2_padding
        self.layer1_out_channels = layer1_out_channels
        self.layer2_out_channels = layer2_out_channels
        self.image_dims = image_dims
        self.filter_size = filter_size
        self.max_pool_size = max_pool_size
        self.stride = stride
        self.dims = self.__getDims()

        # define layers:
        self.layer1 = nn.Conv2d(in_channels=3, out_channels=self.layer1_out_channels, kernel_size=self.filter_size, padding=self.layer1_padding)
        self.layer2 = nn.Conv2d(in_channels=self.layer1_out_channels, out_channels=self.layer2_out_channels, kernel_size=self.filter_size, padding=self.layer2_padding)
        self.layer3 = nn.Linear(in_features=self.layer2_out_channels*self.dims*self.dims, out_features=256)

    def __getDims(self): # assumes square image
        first_conv = (self.image_dims - self.filter_size + 2 * self.layer1_padding) + 1
        first_pool = int((first_conv - self.max_pool_size) / self.stride) + 1
        second_conv = (first_pool - self.filter_size + 2 * self.layer2_padding) + 1
        second_pool = int((second_conv - self.max_pool_size) / self.stride) + 1
        return second_pool

    def forward(self, t):
        # layer 1: each channel passes through relu, then passes through max pooling 2x2, stride 2x2
        t = F.max_pool2d(F.relu(self.layer1(t)), 2, stride=2)
        # layer 2: each channel passes through relu, then passes through max pooling 2x2, stride 2x2
        t = F.max_pool2d(F.relu(self.layer2(t)), 2, stride=2)
        # layer 3: don't need softmax since we're using cross-entropy
        t = t.reshape(-1, self.layer2_out_channels*self.dims*self.dims)
        t = self.layer3(t)
        return t


class NetworkEvaluator:
    def __init__(self, network, train_loader, test_loader, lr=0.001, shuffle=True, epochs=5, accuracy_threshold=0.04):
        self.network = network
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.lr=lr
        self.shuffle=shuffle
        self.epochs=epochs
        self.accuracy_threshold = accuracy_threshold

    def get_accuracy(self, dataloader):
        count=0
        correct=0

        self.network.eval()
        with torch.no_grad():
            for images, labels in dataloader:
                images, labels = images.to(dev), labels.to(dev)
                preds=self.network(images)
                batch_correct=preds.argmax(dim=1).eq(labels).sum().item()
                batch_count=len(images.cpu())
                count+=batch_count
                correct+=batch_correct
        self.network.train()
        return correct/count

    def evaluate(self):
        optimizer = optim.Adam(self.network.parameters(), lr=self.lr)
        self.network.train()
        prevAcc = 0
        for epoch in range(self.epochs):
            for images, labels in self.train_loader:
                images, labels = images.to(dev), labels.to(dev)
                preds = self.network(images)
                loss = F.cross_entropy(preds, labels).to(dev)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            epochAcc = self.get_accuracy(self.train_loader)
            print('Epoch {0}: train set accuracy {1}'.format(epoch, epochAcc))
            if epochAcc - prevAcc < self.accuracy_threshold: break
            else: prevAcc = epochAcc
        testAcc = self.get_accuracy(self.test_loader)
        print('\nTest set accuracy {1}'.format(epoch,testAcc))
        return testAcc


network = Network()
network.to(dev)
train_loader, test_loader = getInfo()
ne = NetworkEvaluator(network, train_loader, test_loader)
ne.evaluate()