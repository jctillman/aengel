
import json
from argparse import ArgumentParser
from jsonschema import validate

def get_settings(settings_path):
    json_file = open(settings_path)
    data = json.load(json_file)
    validate(instance=data, schema=master_schema)
    return data

timed_schema = {
    "type": "object",
    "properties": {
        "time_start": { "type": "string"},
        "timed_end": { "type": "string"},
        "minimum_interval": { "type": "number"},
        "maximum_interval": { "type": "number"}
    },
    "required": ["time_start", "time_end", "minimum_interval", "maximum_interval"]
}    

processs_schema = {
    "type": "object",
    "properties": {
        "command": { "type": "array", "items": { "type": "string" } },
        "timing": timed_schema
    }
}

master_schema = {
    "type": "object",
    "properties": {
        "unlabeled": processs_schema,
        "startup": processs_schema
    }
}



