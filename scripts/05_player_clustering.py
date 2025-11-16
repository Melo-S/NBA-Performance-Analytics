# NBA Player Clustering Script
# This script groups NBA players into 5 different categories based on their stats
# Using K-means clustering algorithm from Apache Spark
# Created by Data Titans team for Milestone 3

from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import ClusteringEvaluator
import pandas as pd
from pymongo import MongoClient

# 1: Set up Apache Spark
# Spark is like a super-powered engine for processing big data
# We need it because regular Python can't handle millions of rows efficiently
spark = SparkSession.builder \
    .appName("NBA Player Clustering") \
    .getOrCreate()

print("Spark session started - ready to analyze NBA data!")

# 2: Load our cleaned NBA data
# We're reading from the JSONL file we created earlier
# This contains all the player stats in a format Spark can understand
df = spark.read.json("data/curated/nba_ready.jsonl")
print(f"Loaded {df.count()} player records from our dataset")

# 3: Prepare the data for clustering
# We need to pick which stats to use for grouping players
# These are the key performance indicators that define different player types
feature_cols = ["stats.points", "stats.rebounds", "stats.assists", "stats.turnovers", "stats.minutes"]

# The VectorAssembler combines all these stats into a single "feature vector"
# Think of it like packing a suitcase - we put all the stats together for each player
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df_features = assembler.transform(df)

print("Prepared features for clustering - each player now has a 'stat fingerprint'")

# 4: Apply K-means clustering
# K-means is like sorting players into 5 groups based on how similar their stats are
# We chose 5 clusters because NBA players typically fall into categories like:
# - Superstars, Role players, Bench players, etc.
kmeans = KMeans().setK(5).setSeed(1)  # 5 clusters, seed=1 for consistent results
model = kmeans.fit(df_features)

print("Training K-means model... this groups similar players together")

# 5: Get the clustering results
# Now each player gets assigned to one of the 5 clusters
predictions = model.transform(df_features)

# 6: Check how good our clustering is
# Silhouette score tells us how well-separated the groups are
# Higher scores (closer to 1.0) mean better clustering
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print(f"Silhouette score: {silhouette:.3f} - this measures clustering quality")

# 7: Show what each cluster represents
# The cluster centers show the "average" stats for players in each group
centers = model.clusterCenters()
print("\nCluster Centers (average stats for each group):")
print("Features: [points, rebounds, assists, turnovers, minutes]")
for i, center in enumerate(centers):
    print(f"Cluster {i}: {center}")

# 8: Save the results
# We save the player names and their cluster assignments
# This creates a Parquet file - it's like a super efficient spreadsheet for big data
predictions.select("player_name", "prediction").write.mode("overwrite").parquet("data/processed/player_clusters.parquet")

print("Results saved! Check data/processed/player_clusters.parquet")
print("Now we can see which players belong to which performance groups")

# Clean up
spark.stop()
print("Spark session closed - all done!")
