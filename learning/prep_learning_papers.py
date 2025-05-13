import pandas as pd
from prep_papers import create_central_df

df = create_central_df("learning_citations.csv")

# Define keyword sets
# keywords for social learning / technology adoption / diffusion
keywords_learning = [
    "social learning", "learning", "diffusion",
    "peer effects", "network effects",
    "information frictions", "spillovers", "role models",
    "share information", "bandwagon effect", "contagion",
    "word-of-mouth", "share", "observational",
    "Bayesian updating", "access to information",
    "diffusion of innovation", "seeding", "complex contagion",
    "network diffusion", "exposure effect", "experimental spillovers",
    "network centrality", "opinion leaders", "sharing information"
]
keywords_rural = [
    "rural", "village", "farming", "smallholder", "agriculture", "household",
    "community", "crop", "pastoral", "livelihood"
]

# Set up flags for relevant papers
def on_learning(text):
    text = text.lower()
    return any(k in text for k in keywords_learning)

def on_rural(text):
    text = text.lower()
    return any(k in text for k in keywords_rural)

df['on_learning'] = df.apply(lambda row: on_learning(row['title'] + " " + row['abstract']), axis=1)
df['on_rural'] = df.apply(lambda row: on_rural(row['title'] + " " + row['abstract']), axis=1)

# New statistics for learning and rural papers
print("-" * 30)
print(f"Total number of papers with abstract (could be more if scraped better / also used open access pdfs): {len(df)}")
print("-" * 30)
print(f"Papers flagged for learning: {df['on_learning'].sum()}")
print(f"Papers flagged for rural: {df['on_rural'].sum()}")
print(f"Papers flagged for both learning AND rural: {(df['on_learning'] & df['on_rural']).sum()}")
print("-" * 30)

#
# # make a csv with only the papers flagged for both risk sharing and rural
df_both = df[df['on_learning'] & df['on_rural']].copy()
df_both.to_csv("final_learning_papers.csv", index=False)