from scripts.main import main
from src.utils.ensure_directories_exist import ensure_directories_exist

if __name__ == "__main__":
    ensure_directories_exist()
    main()
