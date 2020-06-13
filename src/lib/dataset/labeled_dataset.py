
import torch
import glob
from random import randrange
from os import path

from time import sleep
from PIL import Image
import numpy as np

from lib.settings import get_settings
from lib.dataset.dataset_schema import dataset_schema
from lib.dataset.utils import get_categories, get_paths, clip_by_range, zeros_for


class LabeledDataset(torch.utils.data.Dataset):

  def __init__(self, data_dir, sample_answers, size=64, range=[0,1]):
        'Characterizes a dataset for PyTorch'
        self.size = size
        self.categories = get_categories(sample_answers)
        self.data_paths = clip_by_range(get_paths(data_dir), range)
        print("Loading labels...")
        self.all_labels = self._get_all_answers()
        print("Loading images...")
        self.all_images = self._get_all_images()

  def __len__(self):
        'Denotes the total number of samples'
        return len(self.data_paths)

  def __getitem__(self, index):
        'Generates one sample of data'
        png_path, json_path = self.data_paths[index]
        image = self._get_image(index)
        zeros = self.all_labels[index]
        return torch.tensor([image]), zeros

  def _iter_answers(self):
        'Iterate through the classes for each image'
        for _, json_path in self.data_paths:
            yield get_settings(json_path, dataset_schema)["answers"]

  def _iter_image_paths(self):
        'Iterate through each image'
        for png_path, _ in self.data_paths:
            yield png_path

  def _get_all_answers(self):
    labels = []
    for answer in self._iter_answers():
        labels_for_data = zeros_for(self.categories)
        for i, classes in enumerate(self.categories):
            for ii, single_class in enumerate(classes):
                if (single_class == answer[i]):
                    labels_for_data[i][ii] = 1

        for one_hot in labels_for_data:
              if (sum(one_hot) != 1):
                    raise Exception("One-hot encoding failed")
        labels.append(labels_for_data)
    return labels

  def _get_all_images(self):
    images = []
    for png_path in self._iter_image_paths():
        image = Image.open(png_path)
        image = np.asarray(image)[:,:,0:3]
        images.append(image)
    return images

  def frequency(self):
        nums = zeros_for(self.categories)
        for answers in self._iter_answers():
            for i, answer in enumerate(answers):
                index = self.categories[i].index(answer)
                if index < 0:
                    raise Exception("Category not found.")
                nums[i][index] = nums[i][index] + 1
        return nums

  def _get_image(self, index):
        image = self.all_images[index]
        start_slice_height = randrange(0, image.shape[0] - self.size)
        start_slice_length = randrange(0, image.shape[1] - self.size)
        image = image[
              start_slice_height:start_slice_height+self.size,
              start_slice_length:start_slice_length+self.size, :
        ]
        a = Image.fromarray(image)
        image = np.reshape(image, [3, self.size, self.size])
        image = image / 255 - 0.5
        return image


