
from lib.dataset.labeled_dataset import LabeledDataset

def get_loaders(data_dir, questions, input_size):

	loader_train = LabeledDataset(data_dir, questions, range=[0,0.1], size=input_size)
	loader_test = LabeledDataset(data_dir, questions, range=[0.7,1.0], size=input_size)

	return loader_train, loader_test