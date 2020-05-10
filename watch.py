import requests
from bs4 import BeautifulSoup

def get_changes(url, previous_html_text=None):
    # Parse response body to detect page changes. (initial CloudFlare
    # site of interest is 'no-cache, max-age=0' with no provided Etag)
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    #TODO: implement
