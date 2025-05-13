import pandas as pd

df = pd.read_csv("townsend_citations.csv")

# Define keyword sets
keywords_risk = [
    "risk sharing", "informal insurance", "consumption smoothing", "income smoothing",
    "shock coping", "idiosyncratic shocks", "transfers", "safety net",
    "income volatility", "co-insurance", "vulnerability"
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
print(f"Total number of papers: {len(df)}")
print(f"Total number of papers with open-access pdfs: {df['openAccessPdf'].notnull().sum()}")
print("-" * 30)
print(f"Papers flagged for risk: {df['on_risk'].sum()} ({(df['openAccessPdf'].notnull() & df['on_risk']).sum()} with open-access pdfs)")
print(f"Papers flagged for rural: {df['on_rural'].sum()} ({(df['openAccessPdf'].notnull() & df['on_rural']).sum()} with open-access pdfs)")
print(f"Papers flagged for both risk AND rural: {(df['on_risk'] & df['on_rural']).sum()} ({(df['openAccessPdf'].notnull() & df['on_rural'] & df['on_risk']).sum()} with open-access pdfs)")
print("-" * 30)

# sample a few papers from each category to sanity check (risk, rural, both, neither)
def print_sample(df, condition, label):
    sample = df[condition].sample(n=5)[['title', 'abstract']]
    print(f"Sample of papers flagged for {label}:")
    print(sample.to_string(index=False))
    print("-" * 30)

print_sample(df, df['on_rural'], "rural")