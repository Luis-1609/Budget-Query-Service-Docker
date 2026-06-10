from notifications import *
import logging
import traceback

# Initialize the logger
logger = logging.getLogger("Scraper.exceptions")

def handleException(error_message="Fatal error ocurred."):
    # Get the full error details (Stack Trace)
    error_details = traceback.format_exc()
    error_message += " Sending email notification."
    
    logger.error(error_message, exc_info=True)
    try:
        send_error_email(error_details)
    except:
        logger.error("Could not send the email notification.")

    # An error is raised so the current execution is skipped.
    raise RuntimeError("Fatal error ocurred in scraper.")