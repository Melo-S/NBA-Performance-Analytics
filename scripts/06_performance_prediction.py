# NBA Performance Prediction Script
# This script predicts how many points a player will score based on their other stats
# Using Linear Regression from scikit-learn (fallback for PySpark issues)
# Created by Data Titans team for Milestone 3

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path

print("Starting NBA performance prediction analysis...")

# 1: Load our cleaned NBA data
jsonl_file = Path("data/curated/nba_ready.jsonl")

if not jsonl_file.exists():
    print("Error: JSONL file not found at {jsonl_file}")
    print("Please run the data processing pipeline first (scripts 01-03)")
    exit(1)

print("Loading data from {jsonl_file}...")
data = []
with open(jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line))

df = pd.DataFrame(data)
print(f"Loaded {len(df)} player records")

# 2: Prepare the data for prediction
# Filter for meaningful minutes and extract features
filtered_df = df[
    (df['season'] >= 2010) &
    (df['stats'].apply(lambda x: x['minutes'] > 10))
].copy()

# Extract features and target
features = []
targets = []
player_info = []

for _, row in filtered_df.iterrows():
    stats = row['stats']
    features.append([
        stats['rebounds'],
        stats['assists'],
        stats['turnovers'],
        stats['minutes']
    ])
    targets.append(stats['points'])
    player_info.append({
        'player_name': row['player_name'],
        'season': int(row['season']),
        'team': row['team'],
        'actual_points': stats['points']
    })

X = np.array(features)
y = np.array(targets)

print(f"Prepared {len(X)} samples for prediction")
print("Features: rebounds, assists, turnovers, minutes")
print("Target: points scored")

# 3: Split data for training and testing
X_train, X_test, y_train, y_test, info_train, info_test = train_test_split(
    X, y, player_info, test_size=0.2, random_state=42
)
print(f"Training on {len(X_train)} records, testing on {len(X_test)} records")

# 4: Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5: Train the Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

print("Training linear regression model... finding the relationship between stats and points")

# 6: Make predictions
y_pred = lr_model.predict(X_test_scaled)

# 7: Evaluate the model
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"R2 Score: {r2:.3f} - this shows how well we can predict points")
print(f"RMSE: {rmse:.3f} points - average prediction error")

# 8: Show model coefficients
feature_names = ['rebounds', 'assists', 'turnovers', 'minutes']
coefficients = lr_model.coef_
intercept = lr_model.intercept_

print(f"\nModel Equation: points = {intercept:.2f}")
for name, coef in zip(feature_names, coefficients):
    print(f"  + ({coef:.4f} × {name})")

# 9: Show some example predictions
print("\nSample Predictions (Actual vs Predicted points):")
for i in range(min(10, len(y_test))):
    player = info_test[i]
    actual = y_test[i]
    predicted = y_pred[i]
    print(f"{player['player_name']} ({player['season']}): {actual:.1f} actual, {predicted:.1f} predicted")

# 10: Save model results
results = {
    'model_performance': {
        'r2_score': r2,
        'rmse': rmse,
        'training_samples': len(X_train),
        'testing_samples': len(X_test)
    },
    'coefficients': {
        'intercept': intercept,
        'features': dict(zip(feature_names, coefficients.tolist()))
    },
    'sample_predictions': []
}

# Add sample predictions
for i in range(min(20, len(y_test))):
    player = info_test[i]
    results['sample_predictions'].append({
        'player_name': player['player_name'],
        'season': player['season'],
        'team': player['team'],
        'actual_points': float(y_test[i]),
        'predicted_points': float(y_pred[i]),
        'error': float(abs(y_test[i] - y_pred[i]))
    })

output_file = Path("docs/performance_predictions.json")
output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w") as f:
    json.dump(results, f, indent=2, default=str)

print(f"\nResults saved to: {output_file}")
