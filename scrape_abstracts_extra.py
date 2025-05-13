import pandas as pd
import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

### TESTING with selenium ###

# pulls from website directly as second option
def scrape_description_meta(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            meta_names = [
                {"name": "description"},
                {"property": "og:description"},
                {"name": "twitter:description"}
            ]
            for attrs in meta_names:
                meta_tag = soup.find('meta', attrs=attrs)
                if meta_tag and meta_tag.get('content'):
                    return meta_tag['content']
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    return None

def scrape_description_meta_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        meta = None
        for selector in [
            'meta[name="description"]',
            'meta[property="og:description"]',
            'meta[name="twitter:description"]'
        ]:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements and elements[0].get_attribute("content"):
                meta = elements[0].get_attribute("content")
                break
        return meta
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    finally:
        driver.quit()