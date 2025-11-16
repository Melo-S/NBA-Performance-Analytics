# NBA Data Transformation Script
# This script converts our clean CSV data into JSON Lines format
# JSON is perfect for MongoDB and makes the data structure clear
# Created by Data Titans team for Milestone 2/3

import pandas as pd, json
from pathlib import Path
import re

# 1: Set up file paths
INP = Path("data/staging/nba_cleansed.csv")  # Clean data from previous step
OUT = Path("data/curated/nba_ready.jsonl")   # Final format for MongoDB

# Make sure output directory exists
OUT.parent.mkdir(parents=True, exist_ok=True)
# Start fresh
if OUT.exists(): OUT.unlink()

print("Starting data transformation to JSON...")
print(f"Reading from: {INP}")
print(f"Saving to: {OUT}")

def slug(s):
    """Create a URL-friendly version of player names for IDs"""
    # Convert to lowercase, replace special chars with dashes
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower())
    return s.strip("-")  # Remove leading/trailing dashes

# 2: Transform CSV to JSON Lines
# JSON Lines format: one JSON object per line
# This is MongoDB's preferred format for importing large datasets
with open(OUT, "w", encoding="utf-8") as f:
    chunk_count = 0
    for ch in pd.read_csv(INP, chunksize=200_000, low_memory=False):
        chunk_count += 1
        print(f"Transforming chunk {chunk_count}...")

        for _, r in ch.iterrows():
            # Create the JSON record structure
            rec = {
                "player_id": slug(r["player_name"]),  # Unique ID from name
                "player_name": r["player_name"],      # Full display name
                "season": int(r["season"]),           # Year (2010-2024)
                "team": r["team"],                    # Team abbreviation
                "stats": {                            # All performance stats
                    "points": float(r["points"]),
                    "rebounds": float(r["rebounds"]),
                    "assists": float(r["assists"]),
                    "turnovers": float(r["turnovers"]),
                    "minutes": int(r["minutes"]),
                    "fg_pct": float(r["fg_pct"]),
                    "plus_minus": 0.0                # Placeholder for future use
                }
            }

            # Write one JSON object per line
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"JSON transformation complete! Processed {chunk_count} chunks")
print(f"JSONL data saved to: {OUT}")
print(f"Final size: {OUT.stat().st_size / 1024 / 1024:.1f} MB")
print("Data is now ready for MongoDB import!")
print("Each line is a complete player-season record in JSON format")
