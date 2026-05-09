# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

def bronze_update(df, batch_id, target_table):
    final_df = df.withColumn('batch_id', F.lit(batch_id))
    (
    final_df.write
        .mode('overwrite')
        .format('delta')
        .partitionBy('batch_id')
        .option('replaceWhere',f"batch_id = '{batch_id}'")
        .saveAsTable(target_table)
    )