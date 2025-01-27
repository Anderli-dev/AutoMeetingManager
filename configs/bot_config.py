from dotenv import load_dotenv
import os

# Define the path to the .env file located in the parent directory
# This allows sensitive information like API keys to be loaded from a secure environment file
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

# Load environment variables from the specified .env file
load_dotenv(dotenv_path=env_path)

# Retrieve the bot token from environment variables
# Used to authenticate with the Telegram API
bot_token = os.getenv("BOT_TOKEN")

# Retrieve the user ID from environment variables
# Specifies the recipient of bot notifications
user_id = os.getenv("TELEGRAM_USR_ID")
