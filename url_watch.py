import os
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup

# Add webdrivers path
os.environ['PATH'] += ':'+os.path.dirname(os.path.realpath(__file__))+"/webdrivers"

def get_changes(url, wait_string, watch_href_class):
    matching_href = set()
    page_source = ''
    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        with webdriver.Firefox() as driver:
            driver.get(url)
            wait = WebDriverWait(driver, 30) # max-wait
            try:
                load_ui = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, wait_string))
                )
            except Exception as e:
                page_source = driver.page_source
                raise e
            for elem in driver.find_elements_by_class_name(watch_href_class):
                # get full anchor element text
                soup = BeautifulSoup(elem.get_attribute('outerHTML'), 'html.parser')
                full_anchor_element = str(soup.a)
                matching_href.add(full_anchor_element)
            page_source = driver.page_source
        display.stop()
        return {'success': True, "result": matching_href, "debug": page_source}
    except Exception as e:
        return {'success': False, 'msg': page_source+str(e)+traceback.format_exc()}
