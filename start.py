import asyncio

from scripts.main import main
from src.utils.ensure_directories_exist import ensure_directories_exist

# Entry point for the script execution
if __name__ == "__main__":
    try:
        # Ensures that all required directories exist for the program's operation.
        # If any directories are missing, they will be created automatically.
        ensure_directories_exist()

        # Initiates the main asynchronous function to execute the core workflow of the program.
        asyncio.run(main())
    except Exception as e:
        # Handles any exceptions that may arise during the program's execution.
        # Prints the error details to the console for debugging purposes.
        print(f"An error occurred: {e}")
