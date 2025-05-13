import pandas as pd
from scrape_abstracts import *
from tqdm import tqdm
import requests

# load dataset
df = pd.read_csv("data/risk_citations_recovered.csv")

# get rows with missing abstracts
missing = df[df['abstract'].isnull() | (df['abstract'].str.strip() == "")].copy()

# choose paper IDs from DOI or fall back to Semantic Scholar paper ID
def extract_paper_id(row):
    if pd.notnull(row['doi']):
        return row['doi']
    if pd.notnull(row['url']) and '/paper/' in row['url']:
        return row['url'].split('/paper/')[1]
    return None

missing['paper_id'] = missing.apply(extract_paper_id, axis=1)
missing = missing[missing['paper_id'].notnull()].copy()

# initialize results list
recovered_abstracts = []

# track progress using tqdm
print(f"Fetching abstracts for {len(missing)} missing entries...")

for idx, row in tqdm(missing.iterrows(), total=len(missing), desc="Abstracts downloaded"):
    paper_id = row['paper_id']
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}?fields=title,abstract"
    abstract = None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            abstract = response.json().get('abstract')
    except Exception:
        pass

    # Fallback 1: scrape description if abstract is still missing and URL is available
    if not abstract and pd.notnull(row.get('url')):
        abstract = scrape_meta_tags(row['url'])

    # Fallback 2: fetch from CrossRef via DOI
    if not abstract and pd.notnull(row.get('doi')):
        abstract = get_abstract_from_crossref(row['doi'])

    # Fallback 3: get abstract from arXiv
    if not abstract and pd.notnull(row.get('url')):
        abstract = get_arxiv_abstract(row['url'])

    # Fallback 4: get visible text
    if not abstract and pd.notnull(row.get('url')):
        abstract = scrape_visible_abstract(row['url'])

    recovered_abstracts.append(abstract)

# merge recovered abstracts back
missing['recovered_abstract'] = recovered_abstracts
df.loc[missing.index, 'abstract'] = missing['recovered_abstract']

# save updated data
df.to_csv("risk_citations_recovered.csv", index=False)
print("Done. Updated file saved as 'risk_citations_recovered.csv'")