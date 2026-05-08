import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
OUTPUT = "data/processed/news_events_flat.csv"

files = list(RAW_DIR.glob("*.jsonl"))
print("JSONL files found:", len(files))

all_events = []

for file in files:
    print("Reading:", file)
    df_raw = pd.read_json(file, lines=True)

    for _, row in df_raw.iterrows():
        events = row.get("data", [])

        if isinstance(events, list):
            for event in events:
                if isinstance(event, dict):
                    flat = {}

                    flat["event_id"] = event.get("id")
                    flat["type"] = event.get("type")

                    attributes = event.get("attributes", {})
                    relationships = event.get("relationships", {})

                    if isinstance(attributes, dict):
                        for k, v in attributes.items():
                            flat[k] = v

                    if isinstance(relationships, dict):
                        for rel_name, rel_value in relationships.items():
                            flat[f"relationship_{rel_name}"] = str(rel_value)

                    all_events.append(flat)

df = pd.DataFrame(all_events)

print("\n========================")
print("FLATTENED DATASET")
print("========================")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate event_id:")
if "event_id" in df.columns:
    print(df["event_id"].duplicated().sum())
else:
    print("event_id column not found")

print("\nData types:")
print(df.dtypes)

df.to_csv(OUTPUT, index=False)

print("\nSaved flattened CSV:")
print(OUTPUT)