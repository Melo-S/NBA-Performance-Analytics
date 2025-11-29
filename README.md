This project provides a data pipeline to process raw NBA player statistics into a cleaned JSONL format suitable for MongoDB ingestion.

## Prerequisites

- Python 3.x
- Required libraries: `pip install -r requirements.txt`
- Optional: MongoDB Community Edition for full NoSQL functionality
- Optional: PySpark for distributed machine learning algorithms

## Data Pipeline

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

Validate MongoDB import

python scripts/04_validate.py

Export to Parquet for scalable Spark processing

python scripts/07_export_to_parquet.py

Run ML algorithms

python scripts/05_player_clustering.py
python scripts/06_performance_prediction.py

Run NoSQL analytics algorithms

python scripts/08_player_efficiency_ranking.py
python scripts/09_team_performance_analysis.py
python scripts/10_statistical_correlations.py

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

## Web Application (Milestone 4)

The project includes a complete end-to-end web application with interactive data visualizations.

### Running the Web Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask web application
python app.py

# Access the dashboard at: http://localhost:8000
```

### Application Features

- **Interactive Player Search**: Real-time search with career statistics charts
- **Algorithm Execution**: One-click execution of all analytics algorithms
- **Data Visualizations**: Chart.js-powered interactive charts and graphs
- **Scalability Testing**: Performance benchmarking tools
- **Responsive Design**: Works on all devices with Bootstrap styling

### User Queries Supported

1. **Player Search**: Find players and view career statistics
2. **Team Analysis**: Run team performance rankings and trends
3. **Efficiency Rankings**: View top 20 most efficient players
4. **Statistical Correlations**: Analyze relationships between stats
5. **Machine Learning**: Execute clustering and prediction algorithms
6. **Performance Testing**: Benchmark algorithm execution times

## Authors
Data Titans