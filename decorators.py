import functools
import time
from googleapiclient.errors import *
from selenium.common.exceptions import *
from exceptions import *

SELENIUM_TRIES = 10
SELENIUM_DELAY = 0.2

SOFT_SELENIUM_TRIES = 3
SOFT_SELENIUM_DELAY = 0.1

SHEETS_TRIES = 3
SHEETS_INITIAL_DELAY = 10

def selenium_retry(tries=SELENIUM_TRIES, delay=SELENIUM_DELAY):
    def decorator(func):
        @functools.wraps(func) # Keeps the original function's name and metadata
        def wrapper(*args, **kwargs):
            attempt_count = 0
            while attempt_count < tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt_count += 1
                    if delay > 0:
                        time.sleep(delay)
            
            # If we reach here, all retries failed
            # We call the original function one last time to let it raise its error
            # so handleException can catch the specific failure.
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get descriptive info for the error message
                func_name = func.__name__
                # We assume args[1] is by_class and args[2] is element_id
                selector_info = f"{args[1]} {args[2]}" if len(args) > 2 else "unknown selector"
                handleException(f"Failed after {tries} attempts in {func_name} for {selector_info}.")
                #raise RuntimeError("Cycle aborted due to fatal error in Selenium Scraper.")
        return wrapper
    return decorator

def selenium_soft_retry(tries=SOFT_SELENIUM_DELAY, delay=SOFT_SELENIUM_TRIES):
    def decorator(func):
        @functools.wraps(func) # Keeps the original function's name and metadata
        def wrapper(*args, **kwargs):
            attempt_count = 0
            while attempt_count < tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt_count += 1
                    if delay > 0 and attempt_count != tries:
                        time.sleep(delay)
            
            return False
        return wrapper
    return decorator

def sheets_retry(tries=SHEETS_TRIES, initial_delay=SHEETS_INITIAL_DELAY):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt_count = 0
            current_delay = initial_delay
            
            # Initial retry attempts
            while attempt_count < tries:
                try:
                    return func(*args, **kwargs)
                except (HttpError, TimeoutError, ConnectionError):
                    attempt_count += 1
                    if initial_delay > 0:
                        time.sleep(current_delay)
                        current_delay += initial_delay # Incremental backoff
            
            # Final attempt to capture the error for handleException
            try:
                return func(*args, **kwargs)
            except Exception as e:
                func_name = func.__name__
                # Try to extract the range/address from args if available
                resource_info = args[1] if len(args) > 1 else "unknown resource"
                handleException(f"Sheets API failed after {tries + 1} attempts in {func_name} for {resource_info}.")
                #raise RuntimeError("Cycle aborted due to fatal error in Sheets API.")
        return wrapper
    return decorator