import pandas as pd
import json
from pathlib import Path

from llm_checks import load_prompt, fill_prompt, call_llm

INPUT_FILE = "data/processed/news_events_flat.csv"
TRACE_FILE = "logs/llm_traces.jsonl"
OUTPUT_FILE = "data/processed/llm_check_results.json"

Path("logs").mkdir(exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)

semantic_prompt = load_prompt("prompts/semantic_accuracy_v1.md")
entity_prompt = load_prompt("prompts/entity_resolution_v1.md")
source_prompt = load_prompt("prompts/source_relevance_v1.md")

df = pd.read_csv(INPUT_FILE)

# IMPORTANT: Use small sample first
df_sample = df.head(30)

all_results = []

checks = [
    ("semantic_accuracy", semantic_prompt),
    ("entity_resolution", entity_prompt),
    ("source_relevance", source_prompt)
]

print("Running LLM checks on sample records...")
print("Total sample records:", len(df_sample))

for index, row in df_sample.iterrows():
    row_dict = row.to_dict()
    record_id = row_dict.get("event_id", f"row_{index}")

    for check_name, prompt_template in checks:
        prompt = fill_prompt(prompt_template, row_dict)

        result, latency_ms = call_llm(prompt)

        trace = {
            "record_id": record_id,
            "row_number": int(index),
            "check_name": check_name,
            "check_type": "llm",
            "prompt_version": f"{check_name}_v1",
            "model": "gpt-4o-mini",
            "latency_ms": latency_ms,
            "result": result
        }

        all_results.append(trace)

        with open(TRACE_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace) + "\n")

        print(record_id, check_name, result.get("verdict"))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2)

print("\nLLM checks complete.")
print("Saved:", OUTPUT_FILE)
print("Trace log:", TRACE_FILE)