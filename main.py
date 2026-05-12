from functions_main import *
from logger_config import *

# Initialize the logger
logger = CustomLogger(name="Scraper").get_logger()

def main():
    search_available_budget()
    return

if __name__ == "__main__":
    main()