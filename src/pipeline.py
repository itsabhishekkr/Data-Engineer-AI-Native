import pandas as pd
import json
from rule_checks import run_rule_checks
from llm_checks import load_prompt, fill_prompt, call_llm

INPUT = "data/raw/news_events.csv"
OUTPUT = "data/processed/cleaned_news_events.csv"
TRACE_LOG = "logs/llm_traces.jsonl"

semantic_prompt = load_prompt("prompts/semantic_accuracy_v1.md")
entity_prompt = load_prompt("prompts/entity_resolution_v1.md")
source_prompt = load_prompt("prompts/source_relevance_v1.md")

df = pd.read_csv(INPUT)

all_results = []
human_review = []

for _, row in df.iterrows():
    row_dict = row.to_dict()
    record_id = row_dict.get("event_id")

    rule_issues = run_rule_checks(row_dict)

    if rule_issues:
        human_review.append({
            "record_id": record_id,
            "reason": "Rule check failed",
            "issues": rule_issues
        })
        continue

    llm_prompts = [
        ("semantic_accuracy", semantic_prompt),
        ("entity_resolution", entity_prompt),
        ("source_relevance", source_prompt)
    ]

    for check_name, template in llm_prompts:
        prompt = fill_prompt(template, row_dict)
        result, latency_ms = call_llm(prompt)

        trace = {
            "record_id": record_id,
            "check_name": check_name,
            "prompt_version": f"{check_name}_v1",
            "model": "gpt-4o-mini",
            "latency_ms": latency_ms,
            "result": result
        }

        with open(TRACE_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace) + "\n")

        all_results.append(trace)

        if result["verdict"] != "pass" or result["confidence"] < 0.75:
            human_review.append({
                "record_id": record_id,
                "reason": f"{check_name} failed or low confidence",
                "llm_result": result
            })

df.to_csv(OUTPUT, index=False)

with open("data/processed/human_review_queue.json", "w", encoding="utf-8") as f:
    json.dump(human_review, f, indent=2)

print("Pipeline complete")
print("Cleaned data saved:", OUTPUT)
print("Human review records:", len(human_review))