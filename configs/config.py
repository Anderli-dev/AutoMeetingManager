import os
from dotenv import load_dotenv

load_dotenv()

# Define the base directory of the project by going two levels up from the current file's location
BASE_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), "..",  ".."))

LANGUAGE = os.getenv("LANGUAGE")
WHISPER_PROMPT = os.getenv("WHISPER_PROMPT")

_search_words = os.getenv("SEARCH_WORDS", "").split(",")
SEARCH_WORDS = [i.strip() for i in _search_words]
