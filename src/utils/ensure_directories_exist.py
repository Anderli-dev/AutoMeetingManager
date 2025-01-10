import os
from configs import config


def ensure_directories_exist():
    """
    Checks for the existence of specific directories and creates them if they do not exist.

    The directories are specified relative to the base directory defined in the config module.
    """

    # List of directories to check/create, relative to the base directory
    directories = ["data/audiofiles", "data/transcriptions"]

    # Iterate through the list of directories
    for directory in directories:
        # Combine the base directory path with the relative directory path
        parent_directory = os.path.join(config.BASE_DIR, directory)

        # Check if the directory exists
        if not os.path.exists(parent_directory):
            # Create the directory if it does not exist
            os.makedirs(parent_directory)
            print(f"Directory '{parent_directory}' created.")  # Inform user about the created directory
        else:
            # Inform user if the directory already exists
            print(f"Directory '{directory}' already exists.")
