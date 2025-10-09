# ---------------------------------------------------------
# File: data_reduction.py

# Purpose: Reduce the raw NBA dataset to essential columns
# ---------------------------------------------------------

import pandas as pd

def reduce_data(raw_file="nba_raw.csv", output_file="nba_reduced.csv"):
    # Load raw dataset
    df = pd.read_csv(raw_file)
    print("Initial dataset size:", df.shape)

    # Keep only relevant columns
    columns_to_keep = [
        "player_name", "team", "season", "points", "rebounds", "assists",
        "turnovers", "minutes", "fg_pct", "plus_minus", "playoffs_flag"
    ]
    df = df[columns_to_keep]

    # Filter seasons from 2010 onward
    df = df[df["season"] >= 2010]

    # Drop duplicates
    df = df.drop_duplicates(subset=["player_name", "team", "season", "points"])
    print("After reduction:", df.shape)

    # Save reduced file
    df.to_csv(output_file, index=False)
    print(f"✅ Saved reduced dataset to {output_file}")
    return df

if __name__ == "__main__":
    reduce_data()
