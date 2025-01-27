from aiogram import Bot

from configs.bot_config import user_id, bot_token


async def send_message_to_user(text: str):
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=user_id, parse_mode="MarkdownV2",  text=text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()
