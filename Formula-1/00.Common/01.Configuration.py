# Databricks notebook source
catalog_name = 'formula1incr'
bronze_schema = 'bronze'
silver_schema = 'silver'
gold_schema = 'gold'
control_schema = 'control'

# COMMAND ----------

landing_folder_path = '/Volumes/formula1incr/landing/files'

# COMMAND ----------

from pyspark.sql.functions import current_timestamp,col

def add_metadata(df):
    return (df.withColumn("ingestion_timestamp", current_timestamp())
             .withColumn("source_file", col('_metadata.file_path')))
