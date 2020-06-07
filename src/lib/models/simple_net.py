import torch

class SimpleNet(torch.nn.Module):
    def __init__(
          self,
          start_channels=3,
          start_dim=128,
          channel_mult=2,
          output_dims = [2]
          ):
        super(SimpleNet, self).__init__()
        self.start_dim = start_dim
        self.start_channels = start_channels
        self.channel_mult = channel_mult
        current_dim = self.start_dim
        current_channels = self.start_channels
        nns = {}
        while (current_dim > 1):
              nns_name = "conv_"+str(int(current_dim))

              nns[nns_name] = torch.nn.Conv2d(
                    current_channels,
                    current_channels * channel_mult,
                    3, padding=1)

              current_dim = current_dim / 2
              current_channels = current_channels * self.channel_mult

        self.nns = torch.nn.ModuleDict(nns)


        fcs = {}
        for i in range(len(output_dims)):
            fcs_name = 'fcs_' + str(int(i))
            fcs[fcs_name] = torch.nn.Linear(current_channels, output_dims[i])
        self.fcs = torch.nn.ModuleDict(fcs)

    def forward(self, x):
        current_dim = self.start_dim
        current_channels = self.start_channels

        x = x.float()

        while (current_dim > 1):
            nns_name = "conv_"+str(int(current_dim))

            x = self.nns[nns_name](x)
            x = torch.nn.functional.relu(x) 
            x = torch.nn.functional.max_pool2d(x, 2)
            
            current_dim = current_dim / 2
            current_channels = current_channels * self.channel_mult

        x = x.view(-1, current_channels)

        results = []
        for i in range(len(self.fcs.keys())):
            fcs_name = 'fcs_' + str(int(i))
            almost = self.fcs[fcs_name](x)
            result = torch.nn.Softmax(dim=1)(almost)
            
            results.append(result)

        return results