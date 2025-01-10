from scripts.main import main
from src.utils.ensure_directories_exist import ensure_directories_exist

# Check if the script is being executed as the main program
if __name__ == "__main__":
    # Ensure all necessary directories for the program are present
    ensure_directories_exist()

    # Execute the main function to start the program's primary workflow
    main()
