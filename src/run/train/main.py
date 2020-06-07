
import sys
import glob
import torch
import random

from lib.settings import get_settings
from lib.image.get_image import get_image
from lib.models.simple_net import SimpleNet
from lib.dataset.labeled_dataset import LabeledDataset

from run.train.schema import schema

def main():

    settings = get_settings(sys.argv[1], schema)
    data_dir = settings["data_dir"]
    questions = settings["questions"]
    network_size = 32

    loader_train = LabeledDataset(
          data_dir,
          questions,
          range=[0,0.6],
          size=network_size)

    loader_test = LabeledDataset(
          data_dir,
          questions,
          range=[0.6,1.0],
          size=network_size)

    net = SimpleNet(start_channels=3,
          start_dim=network_size,
          channel_mult=3,
          output_dims = [ len(x["answers"]) for x in settings["questions"]])

    #for i in range(len(loader)):
    criterion1 = torch.nn.MSELoss(reduction='sum')
    criterion2 = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(net.parameters(), lr=1e-3)
    train_length = len(loader_train)
    test_length = len(loader_test)

    epochs = 7
    for ii in range(epochs):
      train_total_loss = 0 
      for i in range(train_length):
            inp, labels = loader_train[i]
            out = net(inp)
            loss = criterion1(out[0], torch.tensor([labels[0]]).float()) + criterion2(out[1], torch.tensor([labels[1]]).float())
            if (i % 20 == 0):
                  print("[",i,"/",train_length,"]",loss)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_total_loss = train_total_loss + loss.item()
      print("Train loss:", train_total_loss / train_length)
      test_total_loss = 0
      for i in range(test_length):
            inp, labels = loader_test[i]
            out = net(inp)
            loss = criterion1(out[0], torch.tensor([labels[0]]).float()) + criterion2(out[1], torch.tensor([labels[1]]).float())
            test_total_loss = test_total_loss + loss.item()
      print("Test loss:", test_total_loss / test_length)








