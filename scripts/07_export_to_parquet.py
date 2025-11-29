# NBA Data Export to Parquet Script
# This script converts MongoDB data to Parquet format for scalable Spark processing
# Addresses professor's feedback on scalability - Spark should read from distributed formats
# Created by Data Titans team for Milestone 3 improvements

from pyspark.sql import SparkSession

# 1: Set up Apache Spark
spark = SparkSession.builder \
    .appName("NBA MongoDB to Parquet Export") \
    .getOrCreate()

print("Spark session started - exporting MongoDB data to Parquet...")

# 2: Load data from the JSONL file (which was exported from MongoDB)
# In a production scalable setup, this would read directly from MongoDB using:
# spark.read.format("mongo").option("uri", "mongodb://localhost:27017/nba.player_game_stats").load()
# But for this implementation, we'll convert the existing JSONL to Parquet for demonstration
df = spark.read.json("data/curated/nba_ready.jsonl")
print(f"Loaded {df.count()} player records from MongoDB-exported JSONL")

# 3: Flatten the nested stats structure for easier ML processing
# Convert nested stats.* columns to top-level columns
df_flat = df.select(
    "player_id", "player_name", "season", "team",
    "stats.points", "stats.rebounds", "stats.assists",
    "stats.turnovers", "stats.minutes", "stats.fg_pct"
)

print("Flattened nested stats structure for ML processing")

# 4: Save to Parquet format
# Parquet is columnar, compressed, and optimized for distributed processing
# This creates a scalable data lake format that Spark can efficiently read
df_flat.write.mode("overwrite").parquet("data/processed/nba_player_stats.parquet")

print("Data exported to Parquet format!")
print("Saved to: data/processed/nba_player_stats.parquet")
print("This Parquet file can now be used by Spark ML algorithms for scalable processing")

# 5: Verify the export
df_verify = spark.read.parquet("data/processed/nba_player_stats.parquet")
print(f"Verification: Parquet file contains {df_verify.count()} records")

# Clean up
spark.stop()
