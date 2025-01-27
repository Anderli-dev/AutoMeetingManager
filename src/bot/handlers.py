from aiogram import Bot

from configs.bot_config import user_id, bot_token  # Importing bot token and user ID from configuration


async def send_message_to_user(text: str):
    """
    Asynchronously sends a message to a specific user using the Telegram Bot API.

    Args:
        text (str): The message content to send to the user.

    Behavior:
        - Connects to the Telegram bot using the provided bot token.
        - Sends the message to the user with the specified user ID.
        - Closes the bot session after the operation to release resources.
    """
    # Initialize the bot instance with the token from environment variables
    bot = Bot(token=bot_token)
    try:
        # Send a message to the specified user
        await bot.send_message(chat_id=user_id, parse_mode="MarkdownV2", text=text)
    except Exception as e:
        # Handle and print any errors that occur during the message-sending process
        print(f"Error: {e}")
    finally:
        # Ensure the bot session is properly closed to free up resources
        await bot.session.close()
