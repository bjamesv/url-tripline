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

def get_changes(url, wait_class, watch_class, watch_tag='a'):
    """
    Get dict representing successful scraping of referenced HTML tags

    Returned dict always has 'success' key defined, with boolean value.

    Keyword Arguments:
    url  -- String, representing page to load
    wait_class  -- String, presence of this class name indicates page
        is ready to be searched for target tags
    watch_class  -- String, representing class name of the tags to find
    watch_tag  -- String, representing the type of tags to be found (Default: a)
    """
    matching_tags = set()
    page_source = ''
    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        with webdriver.Firefox() as driver:
            driver.get(url)
            wait = WebDriverWait(driver, 30) # max-wait
            try:
                load_ui = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, wait_class))
                )
            except Exception as e:
                page_source = driver.page_source
                raise e
            for elem in driver.find_elements_by_class_name(watch_class):
                # get full element text
                soup = BeautifulSoup(elem.get_attribute('outerHTML'), 'html.parser')
                full_element = str(soup.find(watch_tag))
                matching_tags.add(full_element)
            page_source = driver.page_source
        display.stop()
        return {'success': True, "result": matching_tags, "debug": page_source}
    except Exception as e:
        return {'success': False, 'msg': page_source+str(e)+traceback.format_exc()}
