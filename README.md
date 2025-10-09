# NBA Performance Analytics

This project provides a data pipeline to process raw NBA player statistics into a cleaned JSON format suitable for MongoDB ingestion.

## Data Pipeline

1. **Data Reduction** (`data_reduction.py`): Filters raw NBA data to essential columns, seasons from 2010 onward.
2. **Data Cleaning** (`data_cleaning.py`): Handles missing values, normalizes data types, standardizes names.
3. **Data Transformation** (`data_transformation.py`): Converts cleaned CSV to JSON with structured player records for database insertion.

## Prerequisites

- Python 3.x
- pandas library: `pip install pandas`

## Usage

1. Place `nba_raw.csv` in the project root.
2. Run the pipeline:
   ```bash
   python data_reduction.py
   python data_cleaning.py
   python data_transformation.py
   ```
3. Outputs:
   - `nba_reduced.csv`: Reduced dataset
   - `nba_cleansed.csv`: Cleaned dataset
   - `nba_ready.json`: JSON for MongoDB

## Data Structure

Each JSON record contains:
- `player_id`: Normalized player identifier
- `player_name`: Player's name
- `season`: Season year
- `team`: Team name
- `stats`: Dictionary of performance stats (points, rebounds, etc.)
- `playoffs_flag`: Boolean indicating playoffs

## Authors
## Data Titans Team