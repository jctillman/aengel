
import sys
import glob
import torch
import random
import numpy as np

from lib.settings import get_settings
from lib.image.get_image import get_image
from lib.models.simple_net import SimpleNet


from run.train.schema import schema
from run.train.get_loaders import get_loaders

def mult(lst):
  i = 1
  for m in list(lst):
    i = i * m
  return i

def do_epoch(net, loader, criteria, optimizer=None, verbose=False):

  length_data = len(loader)
  length_output = len(criteria)

  losses_epoch = [0 for _ in range(length_output)]
  accuracy_epoch = [0 for _ in range(length_output)]

  for i in range(length_data):

    inp, labels = loader[i]
    out = net(inp)

    separated_loss = [
      criteria[i](out[i], torch.tensor([labels[i]]).float())
      for i in range(length_output)
    ]

    for ii in range(length_output):
      predicted = np.argmax(out[ii][0].detach().numpy(), axis=0)
      real =  np.argmax(labels[ii], axis=0)
      if (predicted == real):
        accuracy_epoch[ii] = accuracy_epoch[ii] + 1
    
    if (verbose):
      print("[",i,"/",length_data,"]", end='\r', flush=True)

    if (optimizer):
      optimizer.zero_grad()
      for loss in separated_loss:
        loss.backward(retain_graph=True)


      """        
      n = net.nns["conv_32"].weight.grad
      if n is not None:
        print(mult(n.size()))
        print("32 ", torch.sum(torch.abs(n)) / mult(n.size()))

      n = net.nns["conv_8"].weight.grad
      if n is not None:
        print(mult(n.size()))
        print("8 ", torch.sum(torch.abs(n)) / mult(n.size()))

      n = net.nns["conv_2"].weight.grad
      if n is not None:
        print(mult(n.size()))
        print("2 ", torch.sum(torch.abs(n)) / mult(n.size()))
      """
        

      optimizer.step()

    for i in range(length_output):
      losses_epoch[i] = losses_epoch[i] + separated_loss[i].item()

  if (verbose):
    print("")

  print(".   Accuracy: ", [ x / length_data for x in accuracy_epoch ])

  return [ x / length_data for x in losses_epoch ]


def main():

    settings = get_settings(sys.argv[1], schema)
    questions = settings["questions"]
    data_dir = settings["data_dir"]
    learning_rate = settings["learning_rate"]
    input_size = settings["input_size"]
    channel_mult = settings["channel_mult"]

    loader_train, loader_test = get_loaders(data_dir, questions, input_size)

    net = SimpleNet(start_channels=3,
          start_dim=input_size,
          channel_mult=channel_mult,
          output_dims = [ len(x["answers"]) for x in questions])

    criteria = [torch.nn.MSELoss(reduction='sum') for _ in questions]

    optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)

    epochs = 50
    train_losses = [[] for x in questions]
    test_losses = [[] for x in questions]
    for ii in range(epochs):

      train_losses_epoch = do_epoch(net, loader_train, criteria, optimizer=optimizer, verbose=True)
      print(str(ii), ": Train loss:", train_losses_epoch[0], train_losses_epoch[1])
      for i in range(len(train_losses)):
        train_losses[i].append(train_losses_epoch[i])

      test_losses_epoch = do_epoch(net, loader_test, criteria)
      print(str(ii), ": Test loss:", test_losses_epoch[0], test_losses_epoch[1])
      for i in range(len(train_losses)):
        test_losses[i].append(test_losses_epoch[i])

      if (len(test_losses[0]) >= 2 and any(test[-1] > test[-2] for test in test_losses)):
        pass
        #break

    print(test_losses)
    print(train_losses)
    results = {
      "train_losses": train_losses,
      "test_losses": test_losses,
    }








