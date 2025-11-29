# NBA Performance Analytics - Milestone 4

**Team: Data Titans**  
**Members: Kaleb Kebede, Melvin Sanare, Taylor Tran, Heskiyas Wondaferew**

## 1. User Interface and Data Visualization

We built a web app using Flask with a clean interface. The main page has a search bar at the top for finding players, and below that are cards for different analysis types. Each card has a "Run" button that executes the algorithm and shows results.

The interface includes:
- Player search with autocomplete
- Charts showing player career stats over seasons
- Tables displaying rankings and statistics
- Loading indicators when algorithms run
- Responsive design that works on phones and computers

Users can search for players, click buttons to run analyses, and see results with execution times.

## 2. User Queries and Results

Here are the main ways users interact with our system:

**Player Search**: Type a name like "LeBron James" and get career charts showing points/rebounds/assists by season.

**Team Analysis**: Click button → shows top teams ranked by efficiency with season trends.

**Efficiency Rankings**: Click button → ranks top 20 players by our custom formula.

**Statistical Correlations**: Click button → shows relationships between stats and player role breakdowns.

**ML Algorithms**: Click buttons for clustering (groups similar players) or prediction (estimates points based on other stats).

**Performance Testing**: Click button → shows how fast everything runs with system specs.

All algorithms work and give results in under 3 seconds.

## 3. Scalability

### MongoDB Setup
We designed for MongoDB clusters but used pandas for testing since we had some issues installing MongoDB. Our queries run fast (<1 second) on 9,716 records.

For real clusters we'd use sharding with player_id/season as keys, compound indexes, and 3+ shards for scaling.

### Spark Setup
We implemented ML algorithms using scikit-learn that work the same as PySpark would. For production clusters we'd use Spark with master/worker nodes, HDFS storage, and distributed processing for 5-10x speedup.

### Hardware
**Our setup:**
- Windows 11
- AMD Ryzen 7 (8 cores)
- 32GB RAM, 512GB SSD
- Python 3.13

**Production:** 3-5 nodes with 4-8 cores each, SSD storage, fast networking.

## 4. Source Code

**Main files:**
- `app.py` - Flask web server with API endpoints
- `templates/index.html` - Web interface
- `requirements.txt` - Python packages needed

**Algorithm scripts (10 total):**
- Data processing: reduce, cleanse, transform to JSONL
- Analytics: efficiency rankings, team analysis, correlations
- ML: clustering, prediction, Parquet export
- Validation: MongoDB import checking

### Key Code Examples

**Flask API Endpoint (app.py):**
```python
@app.route('/api/player_efficiency')
def player_efficiency():
    """Get player efficiency rankings"""
    try:
        result = run_algorithm('08_player_efficiency_ranking.py')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
```

**ML Algorithm Implementation (scripts/05_player_clustering.py):**
```python
# Apply K-means clustering
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
cluster_labels = kmeans.fit_predict(X_scaled)

# Evaluate clustering quality
silhouette = silhouette_score(X_scaled, cluster_labels)
print(f"Silhouette score: {silhouette:.3f} - measures clustering quality")
```

**Frontend JavaScript (templates/index.html):**
```javascript
function runAlgorithm(algorithm) {
    fetch(`/api/${algorithm}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                outputDiv.textContent = `✅ Algorithm completed successfully in ${data.execution_time}s\n\n${data.output}`;
            } else {
                outputDiv.textContent = `❌ Algorithm failed:\n${data.error || 'Unknown error'}`;
            }
        });
}
```

**Dependencies (requirements.txt):**
```
flask==3.1.0
pandas==2.3.3
pymongo==4.10.1
psutil==7.1.3
scikit-learn==1.5.1
```

**To run:**
```
pip install -r requirements.txt
python app.py
Go to http://localhost:8000
```

## Peer Evaluation
All team members completed the CATME survey.
