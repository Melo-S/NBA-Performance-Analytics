# NBA Team Performance Analysis Script
# This script analyzes team performance using MongoDB aggregation queries
# Implements Algorithm 4: Team performance analysis with season-over-season comparisons
# Addresses professor's feedback on adding more algorithms beyond Spark MLlib
# Created by Data Titans team for Milestone 3 improvements

import pandas as pd
import json
from pathlib import Path

print("Analyzing NBA team performance using data aggregation...")
print("=" * 60)

# 1: Load data from JSONL file
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

# 2: Filter and aggregate team performance
print("Filtering data and aggregating team performance...")

# Filter for recent seasons and meaningful minutes
filtered_df = df[
    (df['season'] >= 2010) &
    (df['stats'].apply(lambda x: x['minutes'] > 5))
].copy()

# Group by team and season, calculate aggregates
team_stats = filtered_df.groupby(['team', 'season']).agg(
    total_points=('stats', lambda x: x.apply(lambda s: s['points']).sum()),
    total_rebounds=('stats', lambda x: x.apply(lambda s: s['rebounds']).sum()),
    total_assists=('stats', lambda x: x.apply(lambda s: s['assists']).sum()),
    total_turnovers=('stats', lambda x: x.apply(lambda s: s['turnovers']).sum()),
    total_minutes=('stats', lambda x: x.apply(lambda s: s['minutes']).sum()),
    player_count=('player_id', 'count'),
    avg_fg_pct=('stats', lambda x: x.apply(lambda s: s['fg_pct']).mean())
).reset_index()

# Calculate derived metrics
team_stats['points_per_player'] = round(team_stats['total_points'] / team_stats['player_count'], 2)
team_stats['efficiency_rating'] = round(
    (team_stats['total_points'] + team_stats['total_rebounds'] + team_stats['total_assists']) /
    (team_stats['total_turnovers'] + 1),  # Add 1 to avoid division by zero
    2
)
team_stats['avg_fg_pct'] = round(team_stats['avg_fg_pct'], 3)

# Sort by efficiency rating descending
team_stats = team_stats.sort_values('efficiency_rating', ascending=False)

# 3: Prepare results for display and saving
results = []
for _, row in team_stats.iterrows():
    result = {
        "team": row['team'],
        "season": int(row['season']),
        "total_points": int(row['total_points']),
        "points_per_player": row['points_per_player'],
        "efficiency_rating": row['efficiency_rating'],
        "total_rebounds": int(row['total_rebounds']),
        "total_assists": int(row['total_assists']),
        "total_turnovers": int(row['total_turnovers']),
        "player_count": int(row['player_count']),
        "avg_fg_pct": row['avg_fg_pct']
    }
    results.append(result)

# 4: Display results in compact format
print(f"\nTOP 15 Teams by Efficiency (2010-Present)")
print("=" * 85)

for i, team in enumerate(results[:15], 1):  # Show top 15 teams
    print(f"{i:2d}. {team['team']:<3} {team['season']} | PTS:{team['total_points']:4.0f} PPG:{team['points_per_player']:5.1f} EFF:{team['efficiency_rating']:6.2f} | Players:{team['player_count']:2d} FG%:{team['avg_fg_pct']:.1%}")

# 5: Analyze season-over-season trends for top teams
print(f"\nSeason-over-Season Analysis for Top 5 Teams")
print("-" * 50)

top_teams = [result['team'] for result in results[:5]]
for team in top_teams:
    # Filter data for this team and calculate seasonal averages
    team_data = filtered_df[filtered_df['team'] == team].copy()
    if not team_data.empty:
        seasonal_stats = team_data.groupby('season').agg(
            avg_points=('stats', lambda x: x.apply(lambda s: s['points']).mean()),
            avg_rebounds=('stats', lambda x: x.apply(lambda s: s['rebounds']).mean()),
            avg_assists=('stats', lambda x: x.apply(lambda s: s['assists']).mean())
        ).round(1).reset_index().sort_values('season')

        if not seasonal_stats.empty:
            print(f"\n{team} Performance Trends:")
            # Show last 3 seasons
            recent_seasons = seasonal_stats.tail(3)
            for _, row in recent_seasons.iterrows():
                print(f"  {int(row['season'])}: {row['avg_points']:.1f} PTS, {row['avg_rebounds']:.1f} REB, {row['avg_assists']:.1f} AST")

# 6: Save results to JSON file
output_file = Path("docs/team_performance_analysis.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"\nResults saved to: {output_file}")
print("Team performance analysis complete!")
