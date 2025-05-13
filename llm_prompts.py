import re

# prompt for risk-sharing
def build_prompt_risk(title, abstract):
    return f"""
### Instruction:
You are an economic analyst. Based on the following abstract, estimate how successful informal insurance or risk-sharing mechanisms appear to be.

Give your answer as:
- Estimate: a number between 0 and 100 (where 100 = full consumption smoothing and successful risk-sharing, 0 = none)

### Abstract:
{abstract}

### Response:
Estimate:"""

# prompt for learning
def build_prompt_learning(title, abstract):
    return f"""
### Instruction:
You are reviewing research on social learning and technology diffusion in rural development. Based on the abstract, estimate the extent to which learning or adoption occurred among the target population.

Give your answer as:
- Estimate: a number between 0 and 100 (where 100 = full take-up or full awareness and 0 = none)

### Abstract:
{abstract}

### Response:
Estimate:"""

# parsing logic
def parse_response(text):
    match_pct = re.search(r"Estimate:\s*(\d{1,3})", text)
    match_just = re.search(r"Justification:\s*(.*)", text, re.DOTALL)
    estimate = int(match_pct.group(1)) if match_pct else None
    justification = match_just.group(1).strip() if match_just else None
    return estimate, justification
