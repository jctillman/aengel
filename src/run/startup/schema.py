schema = {
    "type": "object",
    "properties": {
        "data_dir": { "type": "string" },
        "resize_factor": {"type": "number"},
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
