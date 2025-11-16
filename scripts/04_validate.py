# NBA Data Validation Script
# This script checks that our data was imported correctly into MongoDB
# We verify the counts and ranges to make sure everything looks good
# Created by Data Titans team for Milestone 2/3

from pymongo import MongoClient

# 1: Connect to our MongoDB database
# This connects to the local MongoDB instance we set up
db = MongoClient("mongodb://localhost:27017").nba

print("🔍 Validating NBA data in MongoDB...")
print("=" * 50)

# 2: Check total number of documents (player-season records)
total_docs = db.player_game_stats.estimated_document_count()
print(f"📊 Total documents: {total_docs:,}")
print("   (Each doc represents one player's stats for one season)")

# 3: Check how many unique players we have
unique_players = len(db.player_game_stats.distinct("player_id"))
print(f"👥 Unique players: {unique_players:,}")

# 4: Check how many different teams are represented
unique_teams = len(db.player_game_stats.distinct("team"))
print(f"🏀 Teams represented: {unique_teams}")

# 5: Check the season range
seasons = db.player_game_stats.distinct("season")
if seasons:
    min_season = min(seasons)
    max_season = max(seasons)
    print(f"📅 Seasons covered: {min_season} - {max_season}")
    print(f"   ({max_season - min_season + 1} years of NBA data)")

print("=" * 50)
print("✅ Data validation complete!")
print("If these numbers look reasonable, our import was successful.")
print("We can now run our machine learning algorithms on this data.")
