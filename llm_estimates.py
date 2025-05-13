import pandas as pd
from tqdm import tqdm
from transformers import pipeline
from llm_prompts import *
import re
import time

def run_LLM(data_csv: str, target_csv_name: str):
    # Load file
    df = pd.read_csv(data_csv)
    df = df[df['abstract'].notnull()].copy()  # take out papers with no abstracts
    df = df[df['abstract'].str.strip() != ""].copy()

    # Hugging Face LLM
    pipe = pipeline("text2text-generation", model="google/flan-t5-small", device_map="auto")

    # Run LLM on each row
    estimates = []
    justifications = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing papers"):
        prompt = build_prompt_risk(row['title'], row['abstract'])
        try:
            response = pipe(prompt, max_new_tokens=64, do_sample=False)[0]['generated_text']
            estimate, justification = parse_response(response)
            estimates.append(estimate)
            justifications.append(justification)
        except Exception:
            estimates.append(None)
            justifications.append(None)

    # Save results
    df['llm_estimate'] = estimates
    df['llm_justification'] = justifications
    df.to_csv(target_csv_name, index=False)
    print("Complete. Results saved to", target_csv_name)

## Run risksharing LLM
current_csv = "risksharing/final_risk_papers.csv"
target_csv = "risksharing/risk_LLM_response.csv"
run_LLM(current_csv, target_csv)

# ## Run learning LLM
# current_csv = "learning/learning_citations.csv"
# target_csv = "learning/learning_LLM_response.csv"
# run_LLM(current_csv, target_csv)