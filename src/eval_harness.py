import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from llm_checks import load_prompt, fill_prompt, call_llm

EVAL_FILE = "evals/semantic_accuracy_eval.csv"
PROMPT_FILE = "prompts/semantic_accuracy_v1.md"

df = pd.read_csv(EVAL_FILE)
prompt_template = load_prompt(PROMPT_FILE)

y_true = []
y_pred = []

for _, row in df.iterrows():
    row_dict = row.to_dict()
    prompt = fill_prompt(prompt_template, row_dict)
    result, latency_ms = call_llm(prompt)

    y_true.append(row_dict["expected_verdict"])
    y_pred.append(result["verdict"])

accuracy = accuracy_score(y_true, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision_score(y_true, y_pred, average="macro", zero_division=0))
print("Recall:", recall_score(y_true, y_pred, average="macro", zero_division=0))