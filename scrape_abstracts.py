import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def safe_get(url, retries=3, timeout=10):
    for _ in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            if r.status_code == 200:
                return r
        except:
            sleep(0.5)
            continue
    return None

def scrape_meta_tags(url):
    try:
        response = safe_get(url)
        if not response:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_keys = [
            {"name": "description"},
            {"name": "og:description"},
            {"property": "og:description"},
            {"name": "twitter:description"},
            {"name": "citation_abstract"},
            {"name": "dc.description"},
            {"property": "dc:description"},
        ]
        for tag in meta_keys:
            meta = soup.find('meta', attrs=tag)
            if meta and meta.get('content'):
                return meta['content'].strip()
    except:
        return None
    return None

def scrape_visible_abstract(url):
    try:
        response = safe_get(url)
        if not response:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        # Look for abstract in class names
        for tag in soup.find_all(['p', 'div']):
            if tag.get('class') and any('abstract' in c.lower() for c in tag.get('class')):
                text = tag.get_text(strip=True)
                if len(text) > 50:
                    return text
        # Try by header
        for header in soup.find_all(['h2', 'h3']):
            if 'abstract' in header.get_text(strip=True).lower():
                sib = header.find_next_sibling(['p', 'div'])
                if sib:
                    text = sib.get_text(strip=True)
                    if len(text) > 50:
                        return text
        # Fallback regex
        text = soup.get_text(separator='\n')
        match = re.search(r'abstract[:\s]*([\s\S]{50,2000})', text, re.IGNORECASE)
        if match:
            candidate = match.group(1).split('\n')[0].strip()
            if len(candidate) > 50:
                return candidate
    except:
        return None
    return None

def get_arxiv_abstract(url):
    try:
        if "arxiv.org" in url:
            m = re.search(r'arxiv\.org/(abs|pdf)/([0-9\.]+)', url)
            if m:
                arxiv_id = m.group(2)
                api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
                resp = safe_get(api_url)
                if resp:
                    soup = BeautifulSoup(resp.content, 'xml')
                    summary = soup.find('summary')
                    if summary:
                        return summary.get_text(strip=True)
    except:
        return None
    return None

def get_abstract_from_crossref(doi):
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = safe_get(url)
        if response:
            data = response.json()
            abstract = data['message'].get('abstract')
            if abstract:
                return BeautifulSoup(abstract, 'lxml').get_text(separator=' ', strip=True)
            return data['message'].get('summary')
    except:
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