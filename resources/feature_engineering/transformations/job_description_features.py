 from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
import dlt
import sys
sys.path.append(spark.conf.get("bundle.sourcePath", "."))

@dp.table(
    name="job_description_features",
    comment="Feature table for job description features"
)
def job_1900_features(input_source="dev.job_prospects.job_1900_silver"):
    df = spark.read.table(input_source)

    feature_cols = [
        "company_size",
        "employment_type",
        "experience",
        "gender",
        "title",
        "job_department",
        "job_field",
        "job_title",
        "job_description",
        "area",
    ]  # label is col "salary"

    assembler = VectorAssembler(inputCols=feature_cols, outputCol="raw_features")
    scaler = StandardScaler(inputCol="raw_features", outputCol="features")

    pipeline = Pipeline(stages=[assembler, scaler])

    model = pipeline.fit(df)
    transformed_df = model.transform(df)

    return transformed_df.select("job_title", "features")
