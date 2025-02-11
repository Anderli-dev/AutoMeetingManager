
from datetime import datetime


def create_filenames():
     # Get the current date and time
    now = datetime.now()
    # Format the date and time as requested
    formatted_datetime = now.strftime("%H-%M_%Y-%m-%d")
    return formatted_datetime