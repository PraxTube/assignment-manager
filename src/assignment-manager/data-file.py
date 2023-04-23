import json
from enum import Enum


class Progress(Enum):
    NOT_STARTED = 0
    JUST_STARTED = 1
    IN_PROGRESS = 2
    ALMOST_DONE = 3
    DONE = 4


def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data
   

def write_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
