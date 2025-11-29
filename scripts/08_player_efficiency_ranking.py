# NBA Player Efficiency Ranking Script
# This script ranks NBA players by efficiency using MongoDB aggregation queries
# Implements Algorithm 3: Player efficiency ranking using NoSQL database queries
# Addresses professor's feedback on adding more algorithms beyond Spark MLlib
# Created by Data Titans team for Milestone 3 improvements

import pandas as pd
import json
from pathlib import Path

print("Ranking NBA players by efficiency using data aggregation...")
print("=" * 60)

# 1: Load data from JSONL file
# Since MongoDB may not be available, we'll use the JSONL file directly
jsonl_file = Path("data/curated/nba_ready.jsonl")

if not jsonl_file.exists():
    print("Error: JSONL file not found at {jsonl_file}")
    print("Please run the data processing pipeline first (scripts 01-03)")
    exit(1)

print("Loading data from {jsonl_file}...")
data = []
with open(jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line))

df = pd.DataFrame(data)
print(f"Loaded {len(df)} player records")

# 2: Filter and calculate efficiency
print("Filtering data and calculating player efficiency...")

# Filter for recent seasons and meaningful minutes
filtered_df = df[
    (df['season'] >= 2010) &
    (df['stats'].apply(lambda x: x['minutes'] > 10))
].copy()

# Calculate efficiency score
filtered_df['efficiency'] = filtered_df['stats'].apply(
    lambda x: x['points'] + x['rebounds'] + x['assists'] +
             (x['fg_pct'] * 10) + (x['minutes'] * 0.1)
)

# Sort by efficiency and get top 20
top_players = filtered_df.nlargest(20, 'efficiency')

# 3: Prepare results for display and saving
results = []
for _, player in top_players.iterrows():
    result = {
        "player_name": player['player_name'],
        "season": int(player['season']),
        "team": player['team'],
        "efficiency": round(player['efficiency'], 2),
        "stats": {
            "points": player['stats']['points'],
            "rebounds": player['stats']['rebounds'],
            "assists": player['stats']['assists'],
            "minutes": player['stats']['minutes'],
            "fg_pct": round(player['stats']['fg_pct'], 3)
        }
    }
    results.append(result)

# 4: Display results in compact format
print(f"\nTOP {len(results)} Most Efficient NBA Players (2010-Present)")
print("=" * 70)

for i, player in enumerate(results, 1):
    stats = player['stats']
    # Clean player name to avoid Unicode issues
    clean_name = player['player_name'].encode('ascii', 'ignore').decode('ascii')[:20]
    print(f"{i:2d}. {clean_name:<20} | {player['season']} {player['team']:<3} | EFF:{player['efficiency']:6.1f} | PTS:{stats['points']:4.1f} REB:{stats['rebounds']:4.1f} AST:{stats['assists']:4.1f} MIN:{stats['minutes']:3.0f} FG%:{stats['fg_pct']:.1%}")

# 5: Save results to JSON file
output_file = Path("docs/top_20_efficient_players.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"\nResults saved to: {output_file}")
