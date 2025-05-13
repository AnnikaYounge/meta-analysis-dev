import pandas as pd
from prep_papers import create_central_df

df = create_central_df("risk_citations_recovered.csv")

# Define keyword sets
keywords_risk = [
    "risk sharing", "insurance", "informal insurance", "consumption smoothing",
    "income smoothing", "shock coping", "idiosyncratic shocks", "transfers", "safety net",
    "income volatility", "co-insurance", "mutual aid", "reciprocity", "insurance markets",
    "household shocks", "risk pooling", "financial inclusion"
]

keywords_rural = [
    "rural", "village", "farming", "smallholder", "agriculture", "household",
    "community", "crop", "pastoral", "livelihood"
]

# Set up flags for relevant papers
def on_risk(text):
    text = text.lower()
    return any(k in text for k in keywords_risk)

def on_rural(text):
    text = text.lower()
    return any(k in text for k in keywords_rural)

df['on_risk'] = df.apply(lambda row: on_risk(row['title'] + " " + row['abstract']), axis=1)
df['on_rural'] = df.apply(lambda row: on_rural(row['title'] + " " + row['abstract']), axis=1)

# New statistics for risk and rural papers
print("-" * 30)
print(f"Total number of papers with abstract (could be more if scraped better / also used open access pdfs): {len(df)}")
print("-" * 30)
print(f"Papers flagged for risk: {df['on_risk'].sum()}")
print(f"Papers flagged for rural: {df['on_rural'].sum()}")
print(f"Papers flagged for both risk AND rural: {(df['on_risk'] & df['on_rural']).sum()}")
print("-" * 30)


# make a csv with only the papers flagged for both risk sharing and rural
df_both = df[df['on_risk'] & df['on_rural']].copy()
df_both.to_csv("final_risk_papers.csv", index=False)