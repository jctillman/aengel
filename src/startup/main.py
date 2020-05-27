
import sys
from uuid import uuid1
from os import path, chdir, getcwd, makedirs

from settings import get_settings
from image.get_image import get_image
from startup.schema import schema

def main():

    settings = get_settings(sys.argv[1], schema)

    base_path = path.join(settings["data_dir"], "startup")
    makedirs(base_path, exist_ok=True)

    new_image = get_image(settings['resize_factor'])
    image_name = uuid1().hex + ".png"
    new_image.save(path.join(base_path, image_name))
    print(image_name)
