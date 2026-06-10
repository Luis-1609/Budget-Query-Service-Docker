import os

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
