from pymongo import MongoClient
db = MongoClient("mongodb://localhost:27017").nba

print("docs:", db.player_game_stats.estimated_document_count())
print("distinct players:", len(db.player_game_stats.distinct("player_id")))
print("distinct teams:", len(db.player_game_stats.distinct("team")))
yrs = db.player_game_stats.distinct("season")
if yrs:
    print("seasons:", min(yrs), "-", max(yrs))
