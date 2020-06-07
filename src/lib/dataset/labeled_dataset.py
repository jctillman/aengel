
import torch
import glob
from random import randrange
from os import path

from PIL import Image
import numpy as np

from lib.settings import get_settings
from lib.dataset.dataset_schema import dataset_schema

class LabeledDataset(torch.utils.data.Dataset):
  'Characterizes a dataset for PyTorch'
  def __init__(self, data_dir, sample_answers, size=128, range=[0,1]):

        self.size = size
        
        categories = [
            [y["key"] for y in x["answers"]] for x in sample_answers
        ]
        self.categories = categories

        data_dir = path.join(data_dir, "labeled")
        png_names = glob.glob(data_dir + "/*.png")
        png_names.sort()
        json_names = glob.glob(data_dir + "/*.json")
        json_names.sort()

        if (len(png_names) != len(json_names)):
            raise Exception("Must have equal input / output fields.")

        data_paths_full = list(zip(png_names, json_names))
        range_start = int(range[0] * len(data_paths_full))
        range_end = int(range[1] * len(data_paths_full))
        self.data_paths = data_paths_full[range_start:range_end]

  def __len__(self):
        'Denotes the total number of samples'
        return len(self.data_paths)

  def __getitem__(self, index):
        'Generates one sample of data'
        png_path, json_path = self.data_paths[index]
        image = Image.open(png_path)
        json = get_settings(json_path, dataset_schema)

        zeros = [ [0 for x in y] for y in self.categories ]
        for i, categories in enumerate(self.categories):
              for ii, category in enumerate(categories):
                    if (category == json["answers"][i]):
                        zeros[i][ii] = 1

        for one_hot in zeros:
              if (sum(one_hot) != 1):
                    raise Exception("One-hot encoding failed")

        image = np.asarray(image)[:,:,0:3]
        shape = image.shape

        start_slice_height = randrange(0, shape[0] - self.size)
        start_slice_length = randrange(0, shape[0] - self.size)
        image = image[
              start_slice_height:start_slice_height+self.size,
              start_slice_length:start_slice_length+self.size, :
        ]

        image = np.reshape(image, [3, self.size, self.size])

        image = image / 128 - 1

        return torch.tensor([image]), zeros