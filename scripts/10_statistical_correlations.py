# NBA Statistical Correlations Script
# This script analyzes correlations between player stats using MongoDB aggregation
# Implements Algorithm 5: Statistical correlations and trends analysis
# Addresses professor's feedback on adding more algorithms beyond Spark MLlib
# Created by Data Titans team for Milestone 3 improvements

import pandas as pd
import json
import numpy as np
from pathlib import Path

print("Analyzing statistical correlations in NBA data...")
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

# 2: Perform correlation analysis using pandas
print("Calculating statistical correlations...")

# Filter for recent seasons and meaningful minutes
filtered_df = df[
    (df['season'] >= 2010) &
    (df['stats'].apply(lambda x: x['minutes'] > 10))
].copy()

# Extract stats into flat columns for correlation analysis
stats_df = pd.DataFrame([row['stats'] for _, row in filtered_df.iterrows()])

# Calculate averages
avg_series = stats_df.mean()
averages = pd.Series({
    'points': round(avg_series['points'], 2),
    'rebounds': round(avg_series['rebounds'], 2),
    'assists': round(avg_series['assists'], 2),
    'turnovers': round(avg_series['turnovers'], 2),
    'minutes': round(avg_series['minutes'], 2),
    'fg_pct': round(avg_series['fg_pct'], 3)
})

# Calculate correlations
correlations = stats_df.corr()
points_rebounds_corr = round(correlations.loc['points', 'rebounds'], 3)
points_assists_corr = round(correlations.loc['points', 'assists'], 3)
turnovers_points_corr = round(correlations.loc['turnovers', 'points'], 3)

print(f"\nStatistical Analysis Results ({len(stats_df)} players)")
print("-" * 50)

print("Average Player Stats:")
print(f"  Points: {averages['points']:.1f}")
print(f"  Rebounds: {averages['rebounds']:.1f}")
print(f"  Assists: {averages['assists']:.1f}")
print(f"  Turnovers: {averages['turnovers']:.1f}")
print(f"  Minutes: {averages['minutes']:.1f}")
print(f"  FG%: {averages['fg_pct']:.3f}")

print("\nCorrelation Coefficients (r):")
print(f"  Points vs Rebounds: {points_rebounds_corr:.3f}")
print(f"  Points vs Assists: {points_assists_corr:.3f}")
print(f"  Turnovers vs Points: {turnovers_points_corr:.3f}")

# Interpret correlations
print("\nCorrelation Insights:")
if abs(points_rebounds_corr) > 0.5:
    print("  • Strong relationship between scoring and rebounding")
if points_assists_corr > 0.3:
    print("  • Players who score tend to also pass well")
if turnovers_points_corr < -0.2:
    print("  • High scorers tend to have fewer turnovers")

# Prepare correlation results for saving
correlation_result = {
    "total_players": len(stats_df),
    "averages": {
        "points": float(averages['points']),
        "rebounds": float(averages['rebounds']),
        "assists": float(averages['assists']),
        "turnovers": float(averages['turnovers']),
        "minutes": float(averages['minutes']),
        "fg_pct": float(averages['fg_pct'])
    },
    "correlations": {
        "points_rebounds": points_rebounds_corr,
        "points_assists": points_assists_corr,
        "turnovers_points": turnovers_points_corr
    }
}

# 3: Analyze performance by position/role
print("\nPerformance Analysis by Player Type")
print("-" * 40)

# Filter for recent seasons
recent_df = df[
    (df['season'] >= 2020) &
    (df['stats'].apply(lambda x: x['minutes'] > 15))
].copy()

# Categorize players by their primary stat contributions
def categorize_role(row):
    stats = row['stats']
    if stats['points'] > 20:
        return "Scorer"
    elif stats['rebounds'] > 8:
        return "Big Man"
    elif stats['assists'] > 6:
        return "Playmaker"
    else:
        return "Role Player"

recent_df['primary_role'] = recent_df.apply(categorize_role, axis=1)

# Group by role and calculate averages
role_stats = recent_df.groupby('primary_role').agg(
    player_count=('player_id', 'count'),
    avg_points=('stats', lambda x: x.apply(lambda s: s['points']).mean()),
    avg_rebounds=('stats', lambda x: x.apply(lambda s: s['rebounds']).mean()),
    avg_assists=('stats', lambda x: x.apply(lambda s: s['assists']).mean()),
    avg_minutes=('stats', lambda x: x.apply(lambda s: s['minutes']).mean())
).round({'avg_points': 1, 'avg_rebounds': 1, 'avg_assists': 1, 'avg_minutes': 1}).reset_index()

# Sort by player count descending
role_stats = role_stats.sort_values('player_count', ascending=False)

role_results = []
for _, row in role_stats.iterrows():
    role_results.append({
        "role": row['primary_role'],
        "player_count": int(row['player_count']),
        "avg_stats": {
            "points": float(row['avg_points']),
            "rebounds": float(row['avg_rebounds']),
            "assists": float(row['avg_assists']),
            "minutes": float(row['avg_minutes'])
        }
    })

print("Player Role Distribution:")
for role in role_results:
    stats = role['avg_stats']
    print(f"  {role['role']}: {role['player_count']} players")
    print(f"    Avg: {stats['points']} PTS, {stats['rebounds']} REB, {stats['assists']} AST, {stats['minutes']} MIN")

# 4: Save comprehensive results
output_data = {
    "correlation_analysis": correlation_result,
    "role_analysis": role_results
}

output_file = Path("docs/statistical_correlations_analysis.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w") as f:
    json.dump(output_data, f, indent=2, default=str)

print(f"\nResults saved to: {output_file}")
print("Statistical correlations analysis complete!")
