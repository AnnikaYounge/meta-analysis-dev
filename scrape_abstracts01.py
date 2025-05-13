import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests


response = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
def scrape_meta_tags(url):
    """Try to extract abstract from various meta tags (description, og:description)."""
    meta_keys = [
        {"name": "description"},
        {"name": "og:description"},
        {"property": "og:description"},
        {"name": "twitter:description"},
        {"name": "citation_abstract"},
        {"name": "dc.description"},
        {"property": "dc:description"},
    ]
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Try several meta tags
            for tag in meta_keys:
                meta_tag = soup.find('meta', attrs=tag)
                if meta_tag and meta_tag.get('content'):
                    return meta_tag['content']
    except:
        return None
    return None

def scrape_visible_abstract(url):
    """Try to extract an abstract-like section from the visible page text."""
    import re
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Look for sections with 'abstract' in the header or class
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
            # Fallback: regex search for 'abstract' followed by text
            text = soup.get_text(separator='\n')
            match = re.search(r'abstract[:\s]*(.{50,2000})', text, re.IGNORECASE)
            if match:
                candidate = match.group(1).split('\n')[0]
                if len(candidate) > 50:
                    return candidate
    except:
        return None
    return None

def get_arxiv_abstract(url):
    """If arXiv, use the API to get the abstract."""
    import re
    try:
        if "arxiv.org" in url:
            arxiv_id = None
            m = re.search(r'arxiv\.org/(abs|pdf)/([0-9\.]+)', url)
            if m:
                arxiv_id = m.group(2)
            if arxiv_id:
                api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
                resp = requests.get(api_url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.content, 'xml')
                    summary = soup.find('summary')
                    if summary:
                        return summary.get_text(strip=True)
    except:
        return None
    return None

def get_abstract_from_crossref(doi):
    """Try to get abstract or summary from CrossRef."""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Try both 'abstract' and 'summary'
            abstract = data['message'].get('abstract')
            if not abstract:
                abstract = data['message'].get('summary')
            return abstract
    except:
        return None
    return None