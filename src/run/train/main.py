
import sys
import glob
import torch
import random
import numpy as np
import time

from lib.settings import get_settings
from lib.models.simple_net import SimpleNet


from run.train.schema import schema
from run.train.get_loaders import get_loaders

def mult(lst):
  i = 1
  for m in list(lst):
    i = i * m
  return i

def do_epoch(net, loader, criteria, optimizer=None, verbose=False, weights=None):

  length_data = len(loader)
  length_output = len(criteria)

  losses_epoch = [0 for _ in range(length_output)]
  accuracy_epoch = [0 for _ in range(length_output)]
  classes_sum = [0 for _ in range(length_output)]
  
  for i in range(length_data):

    start = time.time()
    inp, labels = loader[i]
    #print("Loading: ", time.time() - start)

    start = time.time()
    out = net(inp)

    separated_loss = []
    for ii in range(length_output):
      outt = out[ii]
      label = torch.tensor([labels[ii]]).float()
      weight = weights[ii][torch.argmax(torch.tensor(labels[ii])).item()]
      #print("AAAA ", length_output, ii, weight, label)
      separated_loss.append(criteria[ii](outt, label) * weight)

    for ii in range(length_output):
      classes_sum[ii] = classes_sum[ii] + np.argmax(labels[ii])

    for ii in range(length_output):
      predicted = np.argmax(out[ii][0].detach().numpy(), axis=0)
      real =  np.argmax(labels[ii], axis=0)
      if (predicted == real):
        accuracy_epoch[ii] = accuracy_epoch[ii] + 1
    
    if (verbose and i % 20 == 0):
      print("[",i,"/",length_data,"]", out[0], labels[0], flush=True)

    if (optimizer):
      optimizer.zero_grad()
      for loss in separated_loss:
        loss.backward(retain_graph=True)


      """
      n = net.nns["conv_64"].weight.grad
      if n is not None:
        print(mult(n.size()))
        print("64 ", torch.sum(torch.abs(n)) / mult(n.size()))

      n = net.nns["conv_16"].weight.grad
      if n is not None:
        print(mult(n.size()))
        print("16 ", torch.sum(torch.abs(n)) / mult(n.size()))

      n = net.nns["conv_2"].weight.grad
      if n is not None:
        print(mult(n.size()))
        print("2 ", torch.sum(torch.abs(n)) / mult(n.size()))
      """

      optimizer.step()
      #print("Forward: ", time.time() - start)

    for i in range(length_output):
      losses_epoch[i] = losses_epoch[i] + separated_loss[i].item()

  print(classes_sum)
  if (verbose):
    print("")

  print(".   Accuracy: ", [ x / length_data for x in accuracy_epoch ])

  return [ x / length_data for x in losses_epoch ]


def main():

    print("Main")
    settings = get_settings(sys.argv[1], schema)
    questions = settings["questions"]
    data_dir = settings["data_dir"]
    learning_rate = settings["learning_rate"]
    input_size = settings["input_size"]
    channel_mult = settings["channel_mult"]
    start_channels = settings["start_channels"]
    save_name = settings["save_name"]

    loader_train, loader_test = get_loaders(data_dir, questions, input_size)

    frequency = loader_train.frequency()
    print(frequency)
    weights = [
      [ (sum(x) - y) / sum(x) for y in x ] for x  in frequency
    ]
    print(weights)

    net = SimpleNet(input_channels=3,
          start_channels=start_channels,
          start_dim=input_size,
          channel_mult=channel_mult,
          output_dims = [ len(x["answers"]) for x in questions])

    if ("load_name" in settings):
      print("Loading model...")
      net.load_state_dict(torch.load(settings["load_name"]))

    criteria = [torch.nn.MSELoss() for _ in questions]

    optimizer = torch.optim.SGD(net.parameters(), lr=learning_rate)

    epochs = 50
    train_losses = [[] for x in questions]
    test_losses = [[] for x in questions]
    for ii in range(epochs):

      train_losses_epoch = do_epoch(net, loader_train, criteria, optimizer=optimizer, verbose=True, weights=weights)
      print(str(ii), ": Train loss:", train_losses_epoch[0], train_losses_epoch[1])
      for i in range(len(train_losses)):
        train_losses[i].append(train_losses_epoch[i])

      test_losses_epoch = do_epoch(net, loader_test, criteria, weights=weights)
      print(str(ii), ": Test loss:", test_losses_epoch[0], test_losses_epoch[1])
      for i in range(len(train_losses)):
        test_losses[i].append(test_losses_epoch[i])

      print("Saving model...")
      torch.save(net.state_dict(), save_name)

      if (len(test_losses[0]) >= 2 and any(test[-1] > test[-2] for test in test_losses)):
        pass
        #break

    print(test_losses)
    print(train_losses)
    results = {
      "train_losses": train_losses,
      "test_losses": test_losses,
    }








