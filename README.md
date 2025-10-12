This project provides a data pipeline to process raw NBA player statistics into a cleaned JSONL format suitable for MongoDB ingestion.

## Prerequisites

- Python 3.x
- pandas library: `pip install pandas`
- pymongo library: `pip install pymongo`
- MongoDB Community Edition installed and running on localhost:27017

## Data Pipeline

Note: Do not open or fully read raw CSVs; scripts stream with chunksize.

Process data (streaming)

python scripts/01_reduce.py
python scripts/02_cleanse.py
python scripts/03_transform_to_jsonl.py

Mongo indexes and import

mongosh < create-indexes.js

mongoimport --db nba --collection player_game_stats \
  --file data/curated/nba_ready.jsonl --type json \
  --maintainInsertionOrder --stopOnError \
  --errorFile docs/import_errors.jsonl

Validate

python scripts/04_validate.py

## Outputs

- `data/staging/nba_reduced.csv`: Reduced dataset
- `data/staging/nba_cleansed.csv`: Cleaned dataset
- `data/curated/nba_ready.jsonl`: JSONL for MongoDB
- `docs/import_errors.jsonl`: Import errors (should be empty or tiny)

## Data Structure

Each JSONL record contains:
- `player_id`: Normalized player identifier
- `player_name`: Player's name
- `season`: Season year
- `team`: Team name
- `stats`: Dictionary of performance stats (points, rebounds, etc.)

## Authors
## Data Titans Team
