# NBA Data Reduction Script
# This is the first step in our data pipeline - we take the huge raw NBA dataset
# and reduce it to just the important columns we need for analysis
# Created by Data Titans team for Milestone 2/3

import pandas as pd
from pathlib import Path

# 1: Set up file paths
# We have our raw data from the original download
RAW = Path("data/raw/nba_raw.csv")
# We'll save the cleaned up version here
OUT = Path("data/staging/nba_reduced.csv")

# Make sure the output directory exists
OUT.parent.mkdir(parents=True, exist_ok=True)
# Remove old file if it exists (start fresh)
if OUT.exists(): OUT.unlink()

# 2: Choose which columns we want to keep
# The raw data has tons of columns, but we only need these key stats
usecols = [
    "player","team","season","pts_per_game","trb_per_game",
    "ast_per_game","tov_per_game","mp_per_game","fg_percent"
]

print("Starting data reduction...")
print(f"Reading from: {RAW}")
print(f"Saving to: {OUT}")

def process_chunk(ch):
    """Process one chunk of the CSV file"""
    # Keep only the columns we selected
    ch = ch[usecols].copy()

    # Rename columns to more readable names
    ch = ch.rename(columns={
        "player":"player_name",        # player -> player_name
        "pts_per_game":"points",       # pts_per_game -> points
        "trb_per_game":"rebounds",     # trb_per_game -> rebounds
        "ast_per_game":"assists",      # ast_per_game -> assists
        "tov_per_game":"turnovers",    # tov_per_game -> turnovers
        "mp_per_game":"minutes",       # mp_per_game -> minutes
        "fg_percent":"fg_pct"          # fg_percent -> fg_pct
    })

    # Convert season to numbers and keep only 2010-2024
    # This focuses on recent NBA data (last 15 years)
    ch["season"] = pd.to_numeric(ch["season"], errors="coerce").astype("Int64")
    ch = ch[ch["season"].between(2010, 2024)]

    # Remove duplicate entries (same player, team, season)
    # Sometimes players get traded or data has duplicates
    ch = ch.drop_duplicates(subset=["player_name","team","season"])

    return ch

# 3: Process the file in chunks
# The file is huge (15MB+), so we read it in smaller pieces
# This prevents our computer from running out of memory
first = True
chunk_count = 0
for chunk in pd.read_csv(RAW, chunksize=200_000, usecols=usecols, low_memory=False):
    chunk_count += 1
    print(f"Processing chunk {chunk_count}...")

    out = process_chunk(chunk)
    if not out.empty:
        # Write to CSV - first chunk includes headers, others append
        out.to_csv(OUT, mode="w" if first else "a", index=False, header=first)
        first = False

print(f"Data reduction complete! Processed {chunk_count} chunks")
print(f"Reduced data saved to: {OUT}")
print(f"Final size: {OUT.stat().st_size / 1024 / 1024:.1f} MB")
