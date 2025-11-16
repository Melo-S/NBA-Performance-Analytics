from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("NBA Test") \
    .master("local[*]") \
    .getOrCreate()

print("Spark version:", spark.version)
print("Spark working!")

spark.stop()
