// MongoDB Index Creation Script
// This creates database indexes for faster queries on our NBA data
// Created by Data Titans team for Milestone 2/3

use nba

// Index for player-season lookups (most common query)
db.player_game_stats.createIndex({ player_id: 1, season: 1 })

// Index for team-season aggregations
db.player_game_stats.createIndex({ team: 1, season: 1 })

// Index for top scorer queries (sorted by points descending, then season)
db.player_game_stats.createIndex({ "stats.points": -1, season: 1 })
