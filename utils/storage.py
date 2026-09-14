import json
import os

def load_json(filepath, default=None):
    if default is None:
        default = []

    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return default

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return default


def save_json(filepath, data):
    # Ensure directory exists before saving
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)