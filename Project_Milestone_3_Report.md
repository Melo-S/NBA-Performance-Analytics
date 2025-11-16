# Project Milestone 3 Report – NBA Player Performance Analytics

## Team Name: Data Titans

## Team Members: Kaleb Kebede, Melvin Sanare, Taylor Tran, Heskiyas Wondaferew

## 1. Data Files

For this milestone, we utilized both MongoDB (NoSQL database) and distributed data files for Spark processing. The data was initially stored in MongoDB as described in Milestone 2. For Spark processing, we exported the data to Parquet format, which is optimized for distributed processing.

### Data transformation steps:
1. Read data from MongoDB collection "player_game_stats"
2. Convert to Spark DataFrame
3. Select relevant features for analysis
4. Save as Parquet files for distributed storage

### Sample data (first 3 records from MongoDB):
```json
{
  "player_id": "lebron-james",
  "player_name": "LeBron James",
  "season": 2010,
  "team": "CLE",
  "stats": {
    "points": 29.7,
    "rebounds": 7.3,
    "assists": 8.6,
    "turnovers": 3.4,
    "minutes": 38.8,
    "fg_pct": 0.503
  }
}
```

## 2. Algorithm Description

We implemented two advanced algorithms using Spark's built-in methods:

### Algorithm 1: Player Clustering using K-means (Spark MLlib)
- **Input**: Player performance statistics (points, rebounds, assists, turnovers, minutes)
- **Output**: Cluster assignments for each player (5 clusters representing different player types)
- **Computing operations**: Feature vector assembly, K-means clustering, silhouette evaluation

### Algorithm 2: Performance Prediction using Linear Regression (Spark MLlib)
- **Input**: Player stats excluding points (predictor variables)
- **Output**: Predicted points per game
- **Computing operations**: Feature engineering, train-test split, linear regression training, evaluation

### Pseudo-code for K-means clustering:

```python
def cluster_players(data):
    features = ["stats.points", "stats.rebounds", "stats.assists", "stats.turnovers", "stats.minutes"]
    assembler = VectorAssembler(inputCols=features, outputCol="features")
    feature_data = assembler.transform(data)

    kmeans = KMeans().setK(5).setSeed(1)
    model = kmeans.fit(feature_data)
    predictions = model.transform(feature_data)

    return predictions
```

### Optimization techniques:
- Used Parquet format for efficient columnar storage
- Distributed processing across Spark executors
- Vectorized operations for feature assembly

## 3. Algorithm Results

### K-means Clustering Results:
- **Silhouette score**: 0.57 (good clustering quality)
- **Cluster centers** (features: points, rebounds, assists, turnovers, minutes):
  - Cluster 0: Bench players (2.1 PPG, 1.2 RPG, 0.5 APG, 6.3 MPG)
  - Cluster 1: Elite players (20.9 PPG, 6.2 RPG, 4.6 APG, 34.0 MPG)
  - Cluster 2: Low-minute players (4.9 PPG, 2.6 RPG, 1.1 APG, 14.1 MPG)
  - Cluster 3: Mid-tier players (12.6 PPG, 5.1 RPG, 2.8 APG, 28.8 MPG)
  - Cluster 4: Role players (8.2 PPG, 3.8 RPG, 1.8 APG, 21.4 MPG)

### Linear Regression Results:
- **R² score**: 0.82
- **RMSE**: 2.41 points
- **Execution time**: ~20 seconds on local cluster

### Performance metrics:
- **Clustering**: 0.57 silhouette score on actual dataset
- **Regression**: 0.82 R², 2.41 RMSE on test set

### Results presentation strategy:
- Clustering results stored in Parquet format for on-demand visualization
- Regression model saved for real-time predictions
- Web dashboard planned for Milestone 4 to display results interactively

## 4. Algorithm Scalability

Our algorithms are designed with Big Data scalability in mind:

- **Data partitioning**: Automatic partitioning across Spark executors
- **Memory management**: Spill-to-disk for large datasets
- **Parallel processing**: Map-reduce operations distributed across cluster
- **Fault tolerance**: Automatic task re-execution on node failures

The implementation scales from our current 10MB dataset to the planned 1GB+ datasets by:
- Increasing Spark executor count
- Utilizing HDFS for distributed storage
- Implementing data partitioning strategies
- Using broadcast variables for shared data

## 5. Source Code

Source code is available in the GitHub repository: https://github.com/Melo-S/NBA-Performance-Analytics.git

### Key files:
- `scripts/05_player_clustering.py`: K-means clustering implementation
- `scripts/06_performance_prediction.py`: Linear regression model
- `data/processed/`: Output directories for results

## Peer Evaluation
Completed CATME survey for all team members.
