import os
import json
from enum import Enum


class Progress(Enum):
    NOT_STARTED = 0
    JUST_STARTED = 1
    IN_PROGRESS = 2
    ALMOST_DONE = 3
    DONE = 4


def get_data_file_path():
    return os.path.join(os.path.dirname(__file__), "data.json")


def load_data():
    with open(get_data_file_path(), "r") as f:
        data = json.load(f)
    return data


def write_data(data):
    with open(get_data_file_path(), "w") as f:
        json.dump(data, f, indent=4)
