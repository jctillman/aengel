
import json
from argparse import ArgumentParser
from jsonschema import validate

def get_settings(settings_path, schema):
    json_file = open(settings_path)
    data = json.load(json_file)
    validate(instance=data, schema=schema)
    return data
