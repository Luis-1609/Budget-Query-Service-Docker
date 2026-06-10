import os

# Helper to load .env manually if running locally (e.g. via .bat files on Windows)
for path in [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
    os.path.join(os.path.dirname(__file__), ".env"),
    ".env"
]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip().strip('"').strip("'")
        break

# Web Scraper
WEBSCRAPPING_URL = os.getenv("WEBSCRAPPING_URL", "")
TEST_USERNAME = os.getenv("TEST_USERNAME", "")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")

# Google Sheets
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")

# Mail Notification
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "")
APP_PASSWORD = os.getenv("APP_PASSWORD", "")
