import json
from uuid import uuid1
from datetime import datetime
from os import path, makedirs


def save_to_folder(image, data, base_path):

    makedirs(base_path, exist_ok=True)

    prefix = uuid1().hex
    image_name = prefix + ".png"
    json_name = prefix + ".json"

    image_path = path.join(base_path, image_name)
    json_path = path.join(base_path, json_name)

    image.save(image_path)
    
    date = str(datetime.now())
    write_data = {
        "date": date,
        **data
    }
    with open(json_path, 'w') as out_json:
        json.dump(write_data, out_json)