
import json
from argparse import ArgumentParser
from jsonschema import validate

def get_settings(settings_path):
    json_file = open(settings_path)
    data = json.load(json_file)
    validate(instance=data, schema=unlabeled_schema)
    return data
    
unlabeled_schema = {
    "type": "object",
    "properties": {
        "data_dir": { "type": "string" },
        "resize_factor": {"type": "number"}
    }
}
