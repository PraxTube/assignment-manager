import os
import shutil
from pathlib import Path
import json
from enum import Enum


class Progress(Enum):
    NOT_STARTED = 0
    JUST_STARTED = 1
    IN_PROGRESS = 2
    ALMOST_DONE = 3
    DONE = 4


def is_file(path):
    _, extension = os.path.splitext(path)
    return extension != ""


def file_empty(path):
    return os.stat(path).st_size == 0


def data_file_empty():
    return file_empty(get_data_file_path())


def backup_file_empty():
    return file_empty(get_backup_data_file_path())


def create_path(path):
    if is_file(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        Path(path).touch()
    else:
        os.makedirs(path)


def join(*args):
    path = os.path.join(*args)
    if not os.path.exists(path):
        create_path(path)
    return path


def get_config_dir():
    return join(os.path.expanduser("~"), ".config", "assignment-manager")


def get_data_dir():
    return join(get_config_dir(), "data")


def get_backup_dir():
    return join(get_data_dir(), "backup")


def get_data_file_path():
    return join(get_data_dir(), "data.json")


def get_backup_data_file_path():
    return join(get_backup_dir(), "data.json")


def load_data():
    if data_file_empty():
        raise EOFError(
            "The data file is empty. You should first add assignments before accessing them.",
            get_data_file_path(),
        )
    with open(get_data_file_path(), "r") as f:
        data = json.load(f)
    return data


def write_data(data):
    with open(get_data_file_path(), "w") as f:
        json.dump(data, f, indent=4)


def copy_backup():
    shutil.copyfile(get_data_file_path(), get_backup_data_file_path())


def paste_backup():
    shutil.copyfile(get_backup_data_file_path(), get_data_file_path())
