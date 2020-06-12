
import sys
import glob
import torch
import random

from lib.settings import get_settings
from lib.image.get_image import get_image
from lib.models.simple_net import SimpleNet


from run.train.schema import schema
from run.train.get_loaders import get_loaders

def main():

    settings = get_settings(sys.argv[1], schema)
    data_dir = settings["data_dir"]
    questions = settings["questions"]
    input_size = settings["input_size"]

    loader_train, loader_test = get_loaders(data_dir, questions, input_size)

    net = SimpleNet(start_channels=3,
          start_dim=input_size,
          channel_mult=3,
          output_dims = [ len(x["answers"]) for x in settings["questions"]])

    criteria = [torch.nn.MSELoss(reduction='sum') for _ in questions]


    optimizer = torch.optim.SGD(net.parameters(), lr=1e-3)
    train_length = len(loader_train)
    test_length = len(loader_test)

    

    epochs = 20
    train_losses = [[] for x in questions]
    test_losses = [[] for x in questions]
    for ii in range(epochs):
      train_losses_epoch = [0 for _ in questions]

      for i in range(train_length):
            inp, labels = loader_train[i]
            out = net(inp)
            separated_loss = [
              criteria[i](out[i], torch.tensor([labels[i]]).float())
              for i in range(len(questions))
            ]
            
            if (i % 20 == 0):
                  print("[",i,"/",train_length,"]",separated_loss[0].item(), separated_loss[1].item())
            optimizer.zero_grad()
            for loss in separated_loss:
              loss.backward(retain_graph=True)
            optimizer.step()

            for i in range(len(train_losses)):
              train_losses_epoch[i] = train_losses_epoch[i] + separated_loss[i].item()

      print("Train loss:", train_losses_epoch[0] / train_length, train_losses_epoch[1] / train_length)

      for i in range(len(train_losses)):
        train_losses[i].append(train_losses_epoch[i] / train_length)

      test_losses_epoch = [0 for _ in questions]
      for i in range(test_length):
            inp, labels = loader_test[i]
            out = net(inp)
            separated_loss = [
              criteria[i](out[i], torch.tensor([labels[i]]).float())
              for i in range(len(questions))
            ]

            for i in range(len(train_losses)):
              test_losses_epoch[i] = test_losses_epoch[i] + separated_loss[i].item()

      print("Test loss:", test_losses_epoch[0] / test_length, test_losses_epoch[1] / test_length)
      for i in range(len(train_losses)):
        test_losses[i].append(train_losses_epoch[i] / train_length)

      if (len(test_losses[0]) >= 2 and any(test[-1] > test[-2] for test in test_losses)):
        break
    print(test_losses)
    print(train_losses)
    results = {
      "train_losses": train_losses,
      "test_losses": test_losses,
    }








