import requests
import pandas as pd
import time

# Corpus ID for Townsend (1994)
CORPUS_ID = "153578326"
FIELDS = ",".join([
    "title", "abstract", "authors", "year", "venue", "journal", "externalIds", "url",
    "referenceCount", "citationCount", "influentialCitationCount", "fieldsOfStudy",
    "isOpenAccess", "openAccessPdf", "publicationTypes", "publicationDate", "s2FieldsOfStudy"
])
BASE_URL = f"https://api.semanticscholar.org/graph/v1/paper/CorpusId:{CORPUS_ID}/citations"

# Pagination settings
LIMIT = 100
offset = 0
all_results = []

# Paginate and collect
while True:
    url = f"{BASE_URL}?fields={FIELDS}&limit={LIMIT}&offset={offset}"
    print(f"Fetching {offset}-{offset+LIMIT}...")
    response = requests.get(url)
    if response.status_code != 200:
        print("Error:", response.text)
        break
    batch = response.json().get("data", [])
    if not batch:
        break
    for entry in batch:
        paper = entry["citingPaper"]
        external_ids = paper.get("externalIds")
        doi = external_ids.get("DOI") if external_ids is not None else None
        
        all_results.append({
            "title": paper.get("title"),
            "abstract": paper.get("abstract"),
            "year": paper.get("year"),
            "venue": paper.get("venue"),
            "journal": paper.get("journal", {}).get("name") if paper.get("journal") else None,
            "authors": ", ".join([a["name"] for a in paper.get("authors", [])]),
            "doi": doi,
            "url": paper.get("url"),
            "referenceCount": paper.get("referenceCount"),
            "citationCount": paper.get("citationCount"),
            "influentialCitationCount": paper.get("influentialCitationCount"),
            "fieldsOfStudy": paper.get("fieldsOfStudy"),
            "s2FieldsOfStudy": paper.get("s2FieldsOfStudy"),
            "isOpenAccess": paper.get("isOpenAccess"),
            "openAccessPdf": paper.get("openAccessPdf", {}).get("url") if paper.get("openAccessPdf") else None,
            "publicationTypes": paper.get("publicationTypes"),
            "publicationDate": paper.get("publicationDate")
        })
    offset += LIMIT
    time.sleep(1)

# Save to CSV
df = pd.DataFrame(all_results)
df.to_csv("risk_citations.csv", index=False)
print(f"Saved {len(df)} papers.")