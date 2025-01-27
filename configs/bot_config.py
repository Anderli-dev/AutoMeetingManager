from dotenv import load_dotenv
import os

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')

load_dotenv(dotenv_path=env_path)

bot_token = os.getenv("BOT_TOKEN")
user_id = os.getenv("TELEGRAM_USR_ID")
