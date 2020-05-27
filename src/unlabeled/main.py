
import logging
import time
import sys
from uuid import uuid1
from os import path, chdir, getcwd


from settings import get_settings

from src.image import get_image


def main():
    print(getcwd())
    settings = get_settings(sys.argv[1])
    new_image = get_image(settings['resize_factor'])
    image_name = uuid1().hex + ".png"
    new_image.save(path.join(settings["data_dir"], "unlabeled", image_name))

# Todo:
# Factor out get_image above, to something, whatever

    