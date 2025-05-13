import pandas as pd
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
    pipe = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2", device_map="auto")

    # Run LLM on each row
    estimates = []
    justifications = []

    for _, row in df.iterrows():
        prompt = build_prompt_risk(row['title'], row['abstract'])
        try:
            response = pipe(prompt, max_new_tokens=150, do_sample=False)[0]['generated_text']
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

# ## Run risksharing LLM
# current_csv = "risksharing/risk_citations_recovered.csv"
# target_csv = "risksharing/risk_LLM_response.csv"
# run_LLM(current_csv, target_csv)

# ## Run learning LLM
# current_csv = "learning/learning_citations.csv"
# target_csv = "learning/learning_LLM_response.csv"
# run_LLM(current_csv, target_csv)