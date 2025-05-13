import pandas as pd

def stats_citations(csv):
    # Load CSV
    df = pd.read_csv(csv)

    print("number of papers:", len(df))
    print("number of papers with non-null abstracts:", df['abstract'].notnull().sum())
    # Count papers with missing abstracts
    num_missing_abstracts = df['abstract'].isnull().sum()
    print(f"Number of papers with missing abstracts: {num_missing_abstracts}")

def create_central_df(csv):
    df = pd.read_csv(csv)

    # only keep papers with non-null abstracts or open-access PDFs
    df = df[((df['abstract'].notnull()) & (df['abstract'] != "")) | (df['openAccessPdf'].notnull())].copy()
    # only keep papers with non-null influentialCitationCount
    df = df[df['influentialCitationCount'].fillna(0) > 0].copy()

    # Now convert to string if needed
    df['title'] = df['title'].astype(str)
    df['abstract'] = df['abstract'].astype(str)

    return df

