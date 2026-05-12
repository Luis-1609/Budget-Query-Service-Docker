import time
from datetime import datetime
from logger_config import *
from main import main as run_scraper  

logger = CustomLogger(name="Scraper").get_logger()

START_HOUR = 7
END_HOUR = 19

def run_high_frequency_job():
    logger.info(f"Scheduler Started. Monitoring {START_HOUR}:00-{END_HOUR}:00 window (5s intervals)...")
    
    while True:
        try:
            now = datetime.now()
            
            # Check if we are within the working hours window
            if START_HOUR <= now.hour < END_HOUR:
                run_scraper()
                time.sleep(5) # Waiting time between executions
            else:
                # Handle the "Off-Hours" logic
                logger.debug(f"Current time {now.strftime('%H:%M')} is outside {START_HOUR}:00-{END_HOUR}:00 window. Sleeping...")
                time.sleep(3600) # Sleep for 1 hour
        except Exception as e:
            time.sleep(5) # Cooldown after failed run

if __name__ == "__main__":
    run_high_frequency_job()