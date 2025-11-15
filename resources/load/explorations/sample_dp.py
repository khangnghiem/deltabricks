# Databricks notebook source
import sys

sys.path.append("/Workspace/Users/khangnghiem@gmail.com/deltabricks/resources/load")

# COMMAND ----------

# !!! Before performing any data analysis, make sure to run the pipeline to materialize the sample datasets. The tables referenced in this notebook depend on that step.

display(spark.sql("SELECT * FROM workspace.khangnghiem.sample_trips_load"))
