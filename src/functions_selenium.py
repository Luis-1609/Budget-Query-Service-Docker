from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
from decorators import *
from exceptions import *
import logging

# https://googlechromelabs.github.io/chrome-for-testing/#stable
WAIT_TIME = 3
QUICK_TIME = 0.3

logger = logging.getLogger("Scraper.functions")

def get_chrome_driver():
    try:
        #service = Service(executable_path="chromedriver.exe")
        options = Options()

        # Silence the error messages from Chrome console
        options.add_argument('--log-level=3')

        # Standard configuration to run headless
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1600,900")
        options.add_argument('--disable-translate')
        options.add_argument("--lang=en")

        return webdriver.Chrome(options=options)
    except:
        handleException("Could not get chrome driver.")

@selenium_retry(tries=3, delay=0.1)
def wait_until_present(driver, by_class, element_id, wait_time = WAIT_TIME):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((by_class, element_id)))
    
@selenium_retry(tries=3, delay=0.1)
def wait_until_visible(driver, by_class, element_id, wait_time = WAIT_TIME):
    WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((by_class, element_id)))

@selenium_retry(tries=3, delay=0.1)
def wait_until_stale(driver, table_element, wait_time = WAIT_TIME):
    WebDriverWait(driver, wait_time).until(EC.staleness_of(table_element))

@selenium_retry(tries=3, delay=0.1)
def wait_until_clickable(driver, by_class, element_id, wait_time = WAIT_TIME):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((by_class, element_id)))

@selenium_retry()
def click_element(driver, by_class, element_id):
    driver.find_element(by_class, element_id).click()

@selenium_retry()
def send_keys(driver, by_class, element_id, keys):
    driver.find_element(by_class, element_id).send_keys(keys)

@selenium_retry()
def clear_element(driver, by_class, element_id):
    driver.find_element(by_class, element_id).clear()

@selenium_retry()
def get_element(driver, by_class, element_id):
    return driver.find_element(by_class, element_id)

@selenium_retry()
def get_element(driver, by_class, element_id):
    return driver.find_element(by_class, element_id)

@selenium_retry()
def get_text(driver, by_class, element_id):
    return driver.find_element(by_class, element_id).text

@selenium_retry()
def get_value(driver, by_class, element_id):
    return driver.find_element(by_class, element_id).get_attribute("value")

@selenium_retry()
def get_text_or_value(driver, by_class, element_id):
    try:
        text = driver.find_element(by_class, element_id).text
        if text != "":
            return text
    except:
        pass

    return driver.find_element(by_class, element_id).get_attribute("value")

@selenium_retry()
def select_dropdown_element(driver, by_class, element_id, option):
    dropdown_element = driver.find_element(by_class, element_id)
    select = Select(dropdown_element)
    select.select_by_visible_text(option)

@selenium_retry()
def find_and_click(driver, by_class, element_id):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    driver.find_element(by_class, element_id).click()

@selenium_retry()
def find_and_send(driver, by_class, element_id, keys):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    driver.find_element(by_class, element_id).send_keys(keys)

@selenium_retry()
def find_clear_and_send(driver, by_class, element_id, keys):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    driver.find_element(by_class, element_id).clear()
    driver.find_element(by_class, element_id).send_keys(keys)

@selenium_retry()
def find_and_return(driver, by_class, element_id):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    return driver.find_element(by_class, element_id)

@selenium_retry()
def find_and_return_text(driver, by_class, element_id):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    return driver.find_element(by_class, element_id).text

@selenium_retry()
def find_and_return_value(driver, by_class, element_id):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    return driver.find_element(by_class, element_id).get_attribute("value")

@selenium_retry()
def find_and_return_text_value(driver, by_class, element_id):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    try:
        text = driver.find_element(by_class, element_id).text
        if text != "":
            return text
    except:
        pass

    return driver.find_element(by_class, element_id).get_attribute("value")

@selenium_retry()
def find_and_select(driver, by_class, element_id, option):
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((by_class, element_id)))
    dropdown_element = driver.find_element(by_class, element_id)
    select = Select(dropdown_element)
    select.select_by_visible_text(option)

@selenium_soft_retry()
def is_element_present(driver, by_class, element_id, wait_time = QUICK_TIME):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((by_class, element_id)))
    return True

@selenium_soft_retry()
def is_element_clickable(driver, by_class, element_id, wait_time = QUICK_TIME):
    WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((by_class, element_id)))
    return True

def move_to_last_tab(driver):
    try:
        driver.switch_to.window(driver.window_handles[-1])
    except:
        handleException("Could not move to last tab.")

def count_tabs(driver):
    try:
        return len(driver.window_handles)
    except:
        handleException("Could not count tabs.")
