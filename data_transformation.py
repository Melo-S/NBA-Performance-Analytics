# ---------------------------------------------------------
# File: data_transformation.py
# Author: Kaleb Kebede
# Purpose: Transform cleaned data into JSON for MongoDB ingestion
# ---------------------------------------------------------

import pandas as pd
import json
import re

def normalize_id(name):
    """Generate lowercase alphanumeric player_id."""
    return re.sub(r'[^a-z0-9]', '_', name.lower())

def transform_to_json(input_file="nba_cleansed.csv", output_file="nba_ready.json"):
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
        json.dump(records, f, indent=4)

    print(f"✅ Saved transformed JSON to {output_file}")
    print(f"Total records exported: {len(records)}")

if __name__ == "__main__":
    transform_to_json()
