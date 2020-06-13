schema = {
    "type": "object",
    "properties": {
        "data_dir": { "type": "string" },
        "resize_factor": {"type": "number" },
        "input_size": { "type": "number" },
        "start_channels": { "type": "number" },
        "channel_mult": { "type": "number" },
        "save_name": { "type": "string" },
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": { "type": "string"},
                    "answers": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "key": { "type": "string" },
                                "display": { "type": "string" }
                            }
                        }
                    }
                }
            }
        }
    }
}
