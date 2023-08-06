import pickle
import json
from os.path import isdir, isfile, dirname
from os import listdir
from typing import Dict, Hashable


def load_pickle(pickle_path: str) -> object:
    """Avoid boilerplate pickle loading.

    Args:
        pickle_path (str): Path of pickle file

    Returns:
        object: Python object unpickled
    """
    assert_file_exists(pickle_path)

    with open(pickle_path, "rb") as pf:
        return pickle.load(pf)


def save_pickle(obj: object, pickle_path: str) -> None:
    """Avoid boilerplate pickle saving.

    Args:
        obj (object): desired python object
        pickle_path (str): Path of pickle file
    """
    assert_dir_exists(pickle_path)
    with open(pickle_path, "wb") as pf:
        # protocol 4 is default in python 3.8
        pickle.dump(obj, pf, protocol=4)


def load_json(json_path: str, key_is_int: bool = False) -> Dict[Hashable, object]:
    """Avoid boilerplate json loading.

    Args:
        json_path (str): path to json file
        key_is_int (bool, optional): Convert keys to int. Defaults to False.

    Returns:
        object: a python dict object
    """

    assert_file_exists(json_path)

    with open(json_path, "r") as jf:
        if key_is_int:
            return {int(key): value for key, value in json.load(jf).items()}
        return json.load(jf)


def save_json(obj: Dict[Hashable, object], json_path: str) -> None:
    """Save python dict to json_path

    Args:
        obj (Dict[Hashable, object]): python dict
        json_path (str): path
    """

    assert_dir_exists(json_path)

    with open(json_path, "w") as jf:
        json.dump(obj, jf)


def assert_file_exists(file_path: str) -> None:
    """Assert filepath exists. Give verbose error messages.

    Args:
        file_path (str): file path e.g. abc/xyz.csv or xyz.csv
    """
    dir = dirname(file_path)
    assert dir == "" or isdir(dir), f"{dirname} directory doesn't exist.."
    assert isfile(
        file_path
    ), f"{file_path} is invalid. \nContents of {dir} are {[f for f in listdir(dir)]}"


def assert_dir_exists(file_path: str) -> None:
    """Assert directory of a file_path exists

    Args:
        file_path (str): file path e.g. abc/xyz.csv or xyz.csv
    """
    dir = dirname(file_path)
    assert dir == "" or isdir(dir), f"{dirname} directory doesn't exist.."

