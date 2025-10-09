# ---------------------------------------------------------
# File: data_cleaning.py
# Author: Kaleb Kebede
# Purpose: Clean missing data, fix types, and standardize values
# ---------------------------------------------------------

import pandas as pd

def clean_data(input_file="nba_reduced.csv", output_file="nba_cleansed.csv"):
    df = pd.read_csv(input_file)
    print("Loaded reduced dataset:", df.shape)

    # Fill missing numeric values with 0
    numeric_cols = ["points", "rebounds", "assists", "turnovers", "minutes", "fg_pct", "plus_minus"]
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Fill missing team names
    df["team"] = df["team"].fillna("Unknown Team")

    # Convert FG% to 0–1 range
    df["fg_pct"] = df["fg_pct"].apply(lambda x: x / 100 if x > 1 else x)

    # Convert minutes to int
    df["minutes"] = df["minutes"].astype(int)

    # Standardize team abbreviations
    team_map = {
        "LAL": "Los Angeles Lakers",
        "GSW": "Golden State Warriors",
        "BOS": "Boston Celtics",
        "MIA": "Miami Heat"
    }
    df["team"] = df["team"].replace(team_map)

    # Validate shooting percentage range
    df = df[(df["fg_pct"] >= 0) & (df["fg_pct"] <= 1)]

    # Save cleansed version
    df.to_csv(output_file, index=False)
    print(f"✅ Saved cleaned dataset to {output_file}")
    return df

if __name__ == "__main__":
    clean_data()
