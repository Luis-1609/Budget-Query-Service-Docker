import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, name="ScraperLogger"):
        self.logger = logging.getLogger(name)
        
        # Only configure if the logger doesn't have handlers already
        # This prevents duplicate logs if the class is instantiated twice
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            
            # 1. Create logs directory
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 2. Filename with Date and Time (e.g., 2024-05-20_14-30-05.log)
            # Using dashes/underscores instead of colons (colons are illegal in Windows filenames)
            log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
            log_path = os.path.join(log_dir, log_filename)

            # 3. Create Formatters
            file_format = logging.Formatter('%(asctime)s - [%(levelname)s] - [%(filename)s -> %(funcName)s():%(lineno)d] - %(message)s')
            console_format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

            # 4. File Handler
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(file_format)
            file_handler.setLevel(logging.INFO)

            # 5. Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_format)
            console_handler.setLevel(logging.DEBUG)

            # 6. Add handlers to the logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger