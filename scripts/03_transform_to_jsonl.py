# ---------------------------------------------------------
# File: data_transformation.py
# Purpose: Transform cleaned data into JSON for MongoDB ingestion
# ---------------------------------------------------------

import pandas as pd
import json
import re

def normalize_id(name):
    """Generate lowercase alphanumeric player_id."""
    return re.sub(r'[^a-z0-9]', '_', name.lower())

def transform_to_jsonl(input_file="data/staging/nba_cleansed.csv", output_file="data/curated/nba_ready.jsonl"):
    df = pd.read_csv(input_file)
    print("Loaded cleansed dataset:", df.shape)

    records = []
    for _, row in df.iterrows():
        record = {
            "player_id": normalize_id(row["player_name"]),
            "player_name": row["player_name"],
            "season": row["season"],
            "team": row["team"],
            "stats": {
                "points": float(row["points"]),
                "rebounds": float(row["rebounds"]),
                "assists": float(row["assists"]),
                "turnovers": float(row["turnovers"]),
                "minutes": int(row["minutes"]),
                "fg_pct": float(row["fg_pct"]),
                "plus_minus": float(row["plus_minus"])
            },
            "playoffs_flag": bool(row["playoffs_flag"])
        }
        records.append(record)

    with open(output_file, "w") as f:
        for record in records:
            f.write(json.dumps(record) + '\n')

    print(f"✅ Saved transformed JSON to {output_file}")
    print(f"Total records exported: {len(records)}")

if __name__ == "__main__":
    transform_to_jsonl()
