import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# combine files
# Load the data
risk_classified1 = pd.read_csv("risksharing/data/risk_classified1.csv")
risk_df = pd.read_csv("risksharing/data/risk_classified2.csv")

# Add 'success1' and 'success2' from risk_classified1 to risk_classified2
risk_df['success1'] = risk_classified1['success1']
risk_df['success2'] = risk_classified1['success2']

# Do the same but for the learning files
learn_classified1 = pd.read_csv("learning/data/learning_classified1.csv")
learn_df = pd.read_csv("learning/data/learning_classified2.csv")

# Add 'success1' and 'success2' from learn_classified1 to learn_classified2
learn_df['success1'] = learn_classified1['success1']
learn_df['success2'] = learn_classified1['success2']

# Fields to summarize
fields = [
    "success1", "success2", "benchmark_comparison",
    "distributional_effects", "evidence_strength",
    "mechanism_success", "policy_implication",
    "long_term_effects", "narrative_tone"
]

# Display frequencies
for field in fields:
    print(f"--- {field} ---")
    print("Risk-sharing papers:")
    print(risk_df[field].value_counts(normalize=True))
    print("Learning papers:")
    print(learn_df[field].value_counts(normalize=True))
    print("\n")


def compare_distribution(field):
    combined = pd.concat([
        risk_df[[field]].assign(topic='risk'),
        learn_df[[field]].assign(topic='learning')
    ])
    sns.countplot(data=combined, y=field, hue='topic')
    plt.title(f"Comparison of {field}")
    plt.show()

for field in fields:
    compare_distribution(field)