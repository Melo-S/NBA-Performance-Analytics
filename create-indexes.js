use nba
db.player_game_stats.createIndex({ player_id: 1, season: 1 })
db.player_game_stats.createIndex({ team: 1, season: 1 })
db.player_game_stats.createIndex({ "stats.points": -1, season: 1 })
