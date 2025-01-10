import os
from datetime import datetime


def get_filenames():
    # Define the path to the folder where OBS recordings are saved
    folder_path = "C:/Users/lolke/Videos/OBS"

    # Get today's date in the format YYYY-MM-DD
    today = datetime.now().date()

    # List files that were modified today in the specified folder
    files_today = [
        (f, os.path.getctime(os.path.join(folder_path, f)))  # Store filename and creation time
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and
           datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, f))).date() == today
    ]

    # Sort files by creation time
    files_today_sorted = sorted(files_today, key=lambda x: x[1])

    # Display today's files
    print("Today files:", files_today)

    return files_today_sorted
