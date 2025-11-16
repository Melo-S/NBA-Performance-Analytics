# NBA Data Cleansing Script
# This script takes our reduced data and makes it super clean and consistent
# We fix missing values, standardize formats, and remove bad data
# Created by Data Titans team for Milestone 2/3

import pandas as pd
from pathlib import Path

# 1: Set up file paths
INP = Path("data/staging/nba_reduced.csv")  # Input from reduction step
OUT = Path("data/staging/nba_cleansed.csv")  # Output for next step

# Remove old output file if it exists
if OUT.exists(): OUT.unlink()

print("Starting data cleansing...")
print(f"Reading from: {INP}")
print(f"Saving to: {OUT}")

def normalize_team_name(s):
    """Clean up team names by removing extra spaces"""
    return str(s).strip() if pd.notna(s) else "Unknown Team"

# 2: Process the data in chunks (same as before)
first = True
chunk_count = 0
for ch in pd.read_csv(INP, chunksize=200_000, low_memory=False):
    chunk_count += 1
    print(f"Cleaning chunk {chunk_count}...")

    # Clean player names - remove extra spaces
    ch["player_name"] = ch["player_name"].astype(str).str.strip()

    # Clean team names using our helper function
    ch["team"] = ch["team"].apply(normalize_team_name)

    # Make sure season is a proper number
    ch["season"] = pd.to_numeric(ch["season"], errors="coerce").astype("Int64")

    # 3: Fix the numeric stats
    # Convert to numbers and fill missing values with 0
    # This handles cases where stats weren't recorded
    for c in ["points","rebounds","assists","turnovers","fg_pct"]:
        ch[c] = pd.to_numeric(ch[c], errors="coerce").fillna(0.0).astype(float)

    # Minutes should be whole numbers (integers)
    ch["minutes"] = pd.to_numeric(ch["minutes"], errors="coerce").fillna(0).astype(int)

    # 4: Fix field goal percentages
    # Some data might have percentages as decimals (0.45) or whole numbers (45%)
    # If fg_pct > 1.0, it's probably a percentage, so divide by 100
    ch.loc[ch["fg_pct"] > 1.0, "fg_pct"] = ch["fg_pct"] / 100.0

    # Remove invalid fg_pct values (should be between 0 and 1)
    # Like 0.453 for 45.3% shooting accuracy
    ch = ch[(ch["fg_pct"] >= 0.0) & (ch["fg_pct"] <= 1.0)]

    # 5: Remove rows with missing critical data
    # We can't analyze players without names, teams, or seasons
    ch = ch.dropna(subset=["player_name","team","season"])

    # Remove any remaining duplicates
    ch = ch.drop_duplicates(subset=["player_name","team","season"])

    # Save this cleaned chunk
    ch.to_csv(OUT, mode="w" if first else "a", index=False, header=first)
    first = False

print(f"Data cleansing complete! Processed {chunk_count} chunks")
print(f"Clean data saved to: {OUT}")
print(f"Final size: {OUT.stat().st_size / 1024 / 1024:.1f} MB")
print("Data is now ready for transformation to JSON format!")
