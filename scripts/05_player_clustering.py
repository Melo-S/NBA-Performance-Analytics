# NBA Player Clustering Script
# This script groups NBA players into 5 different categories based on their stats
# Using K-means clustering algorithm from scikit-learn (fallback for PySpark issues)
# Created by Data Titans team for Milestone 3

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import json
from pathlib import Path

print("Starting NBA player clustering analysis...")

# 1: Load our cleaned NBA data
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

# 2: Prepare the data for clustering
# Filter for meaningful minutes and extract stats
filtered_df = df[
    (df['season'] >= 2010) &
    (df['stats'].apply(lambda x: x['minutes'] > 10))
].copy()

# Extract features for clustering
feature_cols = ["points", "rebounds", "assists", "turnovers", "minutes"]
features = []
for _, row in filtered_df.iterrows():
    stats = row['stats']
    features.append([
        stats['points'],
        stats['rebounds'],
        stats['assists'],
        stats['turnovers'],
        stats['minutes']
    ])

X = np.array(features)
print(f"Prepared {len(X)} samples for clustering")

# 3: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Features standardized for better clustering performance")

# 4: Apply K-means clustering
# Using 5 clusters for different player types
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

print("Training K-means model... grouping similar players together")

# 5: Evaluate clustering quality
silhouette = silhouette_score(X_scaled, cluster_labels)
print(f"Silhouette score: {silhouette:.3f} - measures clustering quality")

# 6: Show cluster centers (in original scale)
centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
print("\nCluster Centers (average stats for each group):")
print("Features: [points, rebounds, assists, turnovers, minutes]")
for i, center in enumerate(centers_original):
    print(f"Cluster {i}: [{center[0]:.1f}, {center[1]:.1f}, {center[2]:.1f}, {center[3]:.1f}, {center[4]:.1f}]")

# 7: Add cluster assignments to dataframe
filtered_df['cluster'] = cluster_labels

# 8: Show sample players from each cluster
print("\nSample players from each cluster:")
for cluster_id in range(5):
    cluster_players = filtered_df[filtered_df['cluster'] == cluster_id]
    sample_players = cluster_players.head(3)['player_name'].tolist()
    print(f"Cluster {cluster_id}: {', '.join(sample_players)}")

# 9: Save results to JSON
results = []
for _, row in filtered_df.iterrows():
    result = {
        "player_name": row['player_name'],
        "season": int(row['season']),
        "team": row['team'],
        "cluster": int(row['cluster']),
        "stats": row['stats']
    }
    results.append(result)

output_file = Path("docs/player_clusters.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"\nResults saved to: {output_file}")
