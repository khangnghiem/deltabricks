from pyspark.sql import functions as F
from pyspark import pipelines as dp

@dp.table(name="dev.job_prospects.job_1900_gold")
def latest_job_1900():
    df = spark.read.table("dev.job_prospects.job_1900_silver_inferred")
    max_timestamp = df.agg(F.max("timestamp").alias("max_ts")).collect()[0]["max_ts"]
    return df.filter(F.col("timestamp") == max_timestamp)