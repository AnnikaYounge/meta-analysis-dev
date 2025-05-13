import pandas as pd
from tqdm import tqdm
from transformers import pipeline

# Load zero-shot classifier
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    tokenizer="facebook/bart-large-mnli",
)

def classify_abstract(abstract: str, choices) -> str | None:
    txt = abstract.strip()
    if not txt or txt.lower() == "nan":
        return None
    try:
        result = classifier(
            txt,
            candidate_labels=choices,
            truncation=True,
            max_length=classifier.tokenizer.model_max_length,
            padding=False,
        )
        return result["labels"][0]
    except Exception:
        return None

def run_classifier(data_csv: str, target_csv_name: str, choices_dict: dict):
    df = pd.read_csv(data_csv)
    df = df[df['abstract'].notnull()]
    df = df[df['abstract'].str.strip() != ""]

    for label_name, label_choices in choices_dict.items():
        print(f"Classifying: {label_name}")
        df[label_name] = df['abstract'].apply(
            lambda x: classify_abstract(x, label_choices)
        )

    df.to_csv(target_csv_name, index=False)
    print("Classification complete. Saved to", target_csv_name)


# Define choices for classification
risk_choices_dict = {
    "success1": ["full risk-sharing", "limited risk-sharing"],
    "success2": ["full consumption-smoothing", "limited consumption-smoothing"],
}

learning_choices_dict = {
    "success1": ["everyone informed", "not many informed"],
    "success2": ["full adoption", "limited adoption"],
}

choices_dict = {
    "benchmark_comparison": [
        "matches theoretical benchmark",
        "falls short of benchmark"
    ],

    "distributional_effects": [
        "benefits poorest",
        "benefits middle-income",
        "benefits richest",
        "ambiguous"
    ],

    "evidence_strength": [
        "strong evidence",
        "mixed evidence",
        "weak or inconclusive"
    ],

    "mechanism_success": [
        "risk mitigated through institutions",
        "risk mitigated through networks",
        "risk not effectively mitigated"
    ],

    "policy_implication": [
        "suggests effective intervention",
        "suggests partial intervention",
        "suggests no clear intervention"
    ],

    "long_term_effects": [
        "sustained over time",
        "short-term only",
        "unclear durability"
    ],

    "narrative_tone": [
        "optimistic",
        "neutral",
        "pessimistic"
    ]
}

# run_classifier(
#     data_csv="risksharing/data/final_risk_papers.csv",
#     target_csv_name="risksharing/data/risk_classified1.csv",
#     choices_dict=risk_choices_dict
# )
# run_classifier(
#     data_csv="risksharing/data/final_risk_papers.csv",
#     target_csv_name="risksharing/data/risk_classified2.csv",
#     choices_dict=choices_dict
# )

run_classifier(
    data_csv="learning/data/final_learning_papers.csv",
    target_csv_name="learning/data/learning_classified1.csv",
    choices_dict= learning_choices_dict
)

run_classifier(
    data_csv="learning/data/final_learning_papers.csv",
    target_csv_name="learning/data/learning_classified2.csv",
    choices_dict= choices_dict
)