
import sys
import glob
import torch
from os import path

from settings import get_settings
from image.get_image import get_image

from train.schema import schema

class LabeledDataset(torch.utils.data.Dataset):
  'Characterizes a dataset for PyTorch'
  def __init__(self, data_dir):
        'Initialization'
        data_dir = path.join(data_dir, "labeled")
        
        png_names = glob.glob(data_dir + "/*.png")
        png_names.sort()

        json_names = glob.glob(data_dir + "/*.json")
        json_names.sort()

        if (len(png_names) != len(json_names)):
            raise Exception("Must have equal input / output fields.")

        self.data_paths = list(zip(png_names, json_names))


  def __len__(self):
        'Denotes the total number of samples'
        return len(self.png_names)

  def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample
        png_path, json_path = self.data_paths[index]

        # Load data and get label
        X = torch.load('data/' + ID + '.pt')
        y = self.labels[ID]

        return X, y


def main():

    settings = get_settings(sys.argv[1], schema)
    data_dir = settings["data_dir"]

    loader = LabeledDataset(data_dir)







