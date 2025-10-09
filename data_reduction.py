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
        "player", "team", "season", "pts_per_game", "trb_per_game", "ast_per_game",
        "tov_per_game", "mp_per_game", "fg_percent"
    ]
    df = df[columns_to_keep]

    # Renamed columns to match expected names 
    df = df.rename(columns={
        "player": "player_name",
        "pts_per_game": "points",
        "trb_per_game": "rebounds",
        "ast_per_game": "assists",
        "tov_per_game": "turnovers",
        "mp_per_game": "minutes",
        "fg_percent": "fg_pct"
    })

    # Add missing columns with default values
    df["plus_minus"] = 0.0
    df["playoffs_flag"] = False

    # Filter seasons from 2010 onward
    df = df[df["season"] >= 2010]

    # Dropped duplicates
    df = df.drop_duplicates(subset=["player_name", "team", "season", "points"])
    print("After reduction:", df.shape)

    # Save reduced file
    df.to_csv(output_file, index=False)
    print(f"✅ Saved reduced dataset to {output_file}")
    return df

if __name__ == "__main__":
    reduce_data()
