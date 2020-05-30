
import sys
from os import path

from settings import get_settings
from image.get_image import get_image

from unlabeled.schema import schema
#from popups.get_data import get_data

from save.save_to_folder import save_to_folder

def main():

    settings = get_settings(sys.argv[1], schema)
    base_path = path.join(settings["data_dir"], "unlabeled")

    new_image = get_image(settings['resize_factor'])

    # No data to save with
    # answers = get_data('Questions', settings["questions"])
    data = {}

    save_to_folder(new_image, data, base_path)

    