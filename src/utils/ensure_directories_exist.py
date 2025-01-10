import os
from configs import config

def ensure_directories_exist():
    """
    Checks for the existence of directories and creates them in the parent folder if they do not exist.

    :param directories: List of directory paths to check/create.
    """
    directories = ["data/audiofiles", "data/transcriptions"]
    for directory in directories:
        parent_directory = os.path.join(config.BASE_DIR, directory)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
            print(f"Directory '{parent_directory}' created.")
        else:
            print(f"Directory '{directory}' already exists.")
