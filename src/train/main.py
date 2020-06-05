
import sys
import glob
import torch
import random
from settings import get_settings
from image.get_image import get_image

from models.simple_net import SimpleNet
from dataset.labeled_dataset import LabeledDataset

from train.schema import schema

def main():

    settings = get_settings(sys.argv[1], schema)
    data_dir = settings["data_dir"]
    questions = settings["questions"]

    loader = LabeledDataset(data_dir, questions, output_width=64, output_height=64)

    net = SimpleNet(start_channels=3,
          start_dim=64,
          channel_mult=3,
          output_dims = [ len(x["answers"]) for x in settings["questions"]])

    #for i in range(len(loader)):
    criterion1 = torch.nn.MSELoss(reduction='sum')
    criterion2 = torch.nn.MSELoss(reduction='sum')
    optimizer = torch.optim.SGD(net.parameters(), lr=1e-4)
    for i in range(20):
      inp, labels = loader[i]
      out = net(inp)
      loss = criterion1(out[0], torch.tensor([labels[0]]).float()) + criterion2(out[1], torch.tensor([labels[1]]).float())
      print(loss)
      optimizer.zero_grad()
      loss.backward()
      optimizer.step()








