import pandas as pd
import json

from rule_checks import run_rule_checks

INPUT_FILE = "data/processed/news_events_flat.csv"

OUTPUT_FILE = "data/processed/rule_check_results.json"

SUMMARY_FILE = "data/processed/rule_check_summary.csv"

# Read flattened dataset
df = pd.read_csv(INPUT_FILE)

all_results = []

print("===================================")
print("RUNNING RULE-BASED QUALITY CHECKS")
print("===================================")

print("\nTotal records:", len(df))

# Process each row
for index, row in df.iterrows():

    row_dict = row.to_dict()

    record_id = row_dict.get(
        "event_id",
        f"row_{index}"
    )

    issues = run_rule_checks(row_dict)

    if issues:

        for issue in issues:

            result = {
                "record_id": record_id,
                "row_number": index,
                **issue
            }

            all_results.append(result)

# Create summary
if len(all_results) > 0:

    df_results = pd.DataFrame(all_results)

    summary = (
        df_results
        .groupby(["check_name", "verdict"])
        .size()
        .reset_index(name="count")
    )

else:

    summary = pd.DataFrame(
        columns=[
            "check_name",
            "verdict",
            "count"
        ]
    )

# Save JSON results
with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_results,
        f,
        indent=2
    )

# Save CSV summary
summary.to_csv(
    SUMMARY_FILE,
    index=False
)

print("\n===================================")
print("RULE CHECKS COMPLETE")
print("===================================")

print("\nTotal issues found:")
print(len(all_results))

print("\nSummary:")
print(summary)

print("\nSaved files:")
print(OUTPUT_FILE)
print(SUMMARY_FILE)