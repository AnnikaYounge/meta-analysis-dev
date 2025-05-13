import requests
import pandas as pd
import time

CORPUS_ID_1 = "3993822" # Corpus ID for Learning by Doing and Learning from Others
CORPUS_ID_2 = "1881319" # Corpus ID for Learning About a New Technology: Pineapple in Ghana
CORPUS_ID_3 = "10504196" # Corpus ID for The Diffusion of Microfinance

FIELDS = ",".join([
    "title", "abstract", "authors", "year", "venue", "journal", "externalIds", "url",
    "referenceCount", "citationCount", "influentialCitationCount", "fieldsOfStudy",
    "isOpenAccess", "openAccessPdf", "publicationTypes", "publicationDate", "s2FieldsOfStudy"
])
BASE_URL_1 = f"https://api.semanticscholar.org/graph/v1/paper/CorpusId:{CORPUS_ID_1}/citations"
BASE_URL_2 = f"https://api.semanticscholar.org/graph/v1/paper/CorpusId:{CORPUS_ID_2}/citations"
BASE_URL_3 = f"https://api.semanticscholar.org/graph/v1/paper/CorpusId:{CORPUS_ID_3}/citations"

# Pagination settings
LIMIT = 100
offset = 0
all_results = []

# Paginate and collect
for base_url in [BASE_URL_1, BASE_URL_2, BASE_URL_3]:
    while True:
        url = f"{base_url}?fields={FIELDS}&limit={LIMIT}&offset={offset}"
        print(f"Fetching {offset}-{offset + LIMIT}...")
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
df = df.drop_duplicates(subset=["doi", "url"])
df.to_csv("learning_citations.csv", index=False)
print(f"Saved {len(df)} papers.")