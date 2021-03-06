
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

schema = {
    "type": "object",
    "properties": {
        "unlabeled": processs_schema,
        "startup": processs_schema
    }
}



