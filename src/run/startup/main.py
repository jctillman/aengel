
import sys
from os import path

from lib.settings import get_settings
from lib.image.get_image import get_image
from lib.popups.get_data import get_data
from lib.save.save_to_folder import save_to_folder

from run.startup.schema import schema

def main():

    settings = get_settings(sys.argv[1], schema)
    base_path = path.join(settings["data_dir"], "labeled")

    new_image = get_image(settings['resize_factor'])

    # Get answers to save with
    answers = get_data('Questions', settings["questions"])
    
    if answers is not None:
        data = { "answers": answers }
        save_to_folder(new_image, data, base_path)





