import json
import os

## WRITE FILE ######################################################
def write_file_json(filepath, data):
    """
    Write to `filepath` with `data` JSON format.

    Args:
        filepath    <string>    path of file
        data        <dict>      content of file

    Returns: no
    """
    with open(filepath, "w") as file_handle:
        # file_handle.write(data)
        json.dump(data, file_handle, ensure_ascii=False, indent=4)


def load_json(json_path):
    """
    Load the JSON file from the given path.
    """
    json_obj = None
    with open(json_path) as config_file:
        json_obj = json.load(config_file)
    return json_obj