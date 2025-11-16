# NBA Performance Prediction Script
# This script predicts how many points a player will score based on their other stats
# Using Linear Regression - a classic machine learning algorithm
# Created by Data Titans team for Milestone 3

from pyspark.sql import SparkSession
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

# 1: Set up Apache Spark
# Same as clustering - we need Spark's power for machine learning on big datasets
spark = SparkSession.builder \
    .appName("NBA Performance Prediction") \
    .getOrCreate()

print("Spark session started - ready to predict NBA player points!")

# 2: Load our NBA data
# Using the same cleaned dataset from our data pipeline
df = spark.read.json("data/curated/nba_ready.jsonl")
print(f"Loaded {df.count()} player records for prediction training")

# 3: Prepare the data structure
# Our JSON has nested stats, so we flatten them out
# This makes it easier for the machine learning algorithm to work with
df = df.select("player_id", "player_name", "season", "team", "stats.*")
print("Flattened the nested stats structure")

# 4: Choose features for prediction
# We're trying to predict POINTS using other stats as clues
# Like: if a player grabs lots of rebounds and plays many minutes, they might score more
feature_cols = ["rebounds", "assists", "turnovers", "minutes"]

# VectorAssembler packages these features together for each player
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
df_features = assembler.transform(df)

print("Prepared features - using rebounds, assists, turnovers, and minutes to predict points")

# 5: Split data for training and testing
# We use 80% of data to teach the model, 20% to test how well it learned
# randomSplit ensures we get a random mix, seed=1 makes results reproducible
train_data, test_data = df_features.randomSplit([0.8, 0.2], seed=1)
print(f"Training on {train_data.count()} records, testing on {test_data.count()} records")

# 6: Train the Linear Regression model
# Linear regression finds the mathematical relationship: points = a*rebounds + b*assists + c*turnovers + d*minutes + e
# The model "learns" the best values for a, b, c, d, e from our training data
lr = LinearRegression(featuresCol="features", labelCol="points")
lr_model = lr.fit(train_data)

print("Training linear regression model... finding the relationship between stats and points")

# 7: Test the model
# Now we use the model to predict points for players it hasn't seen before (test set)
predictions = lr_model.transform(test_data)

# 8: Evaluate how good our predictions are
# R² score: How much of the variation in points can we explain? (higher is better, max 1.0)
# RMSE: Average prediction error in points (lower is better)
evaluator = RegressionEvaluator(labelCol="points", predictionCol="prediction", metricName="r2")
r2 = evaluator.evaluate(predictions)

evaluator_rmse = RegressionEvaluator(labelCol="points", predictionCol="prediction", metricName="rmse")
rmse = evaluator_rmse.evaluate(predictions)

print(f"R2 Score: {r2:.3f} - this shows how well we can predict points")
print(f"RMSE: {rmse:.3f} points - average prediction error")

# 9: Show some example predictions
# Let's see how our model did on a few real players
print("\nSample Predictions (Actual vs Predicted points):")
predictions.select("player_name", "points", "prediction").show(10)

# 10: Save the trained model
# This saves our "learned" relationship so we can use it later
lr_model.write().overwrite().save("models/performance_prediction_model")

print("Model saved! We can now predict NBA player points using their other stats")
print("Check models/performance_prediction_model for the saved model")

# Clean up
spark.stop()
print("Spark session closed - prediction complete!")

</final_file_content>

IMPORTANT: For any future changes to this file, use the final_file_content shown above as your reference. This content reflects the current state of the file, including any auto-formatting (e.g., if you used single quotes but the formatter converted them to double quotes). Always base the SEARCH/REPLACE on this final version.
