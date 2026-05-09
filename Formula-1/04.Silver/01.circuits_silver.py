# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/03.silver_helper

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.circuits"
silver_table = f"{catalog_name}.{silver_schema}.circuits"

# COMMAND ----------

from pyspark.sql.functions import col, upper

# COMMAND ----------

circuits_df = spark.read.table(bronze_table).filter(col("batch_id") == v_batch_id)

# COMMAND ----------


circuits_selected_df = circuits_df.select(
                    col("circuitId"),
                    col("circuitName"),
                    col("country"),
                    col("lat"),
                    col("long"),
                    col("locality"),
                    col("ingestion_timestamp"),
                    col("source_file"),
                    col("batch_id")
                    )

# COMMAND ----------

circuits_renamed_df = circuits_selected_df.withColumnsRenamed({"circuitId": "circuit_id", "circuitName": "circuit_name", "lat": "latitude", "long": "longitude"})

# COMMAND ----------

circuits_valid_df = circuits_renamed_df.filter(col("circuit_id").isNotNull())

# COMMAND ----------

circuits_distinct_df = circuits_valid_df.dropDuplicates()

# COMMAND ----------

from pyspark.sql import functions as F
circuits_final_df = circuits_distinct_df.withColumn("circuit_name",F.initcap(F.col("circuit_name"))) \
                                     .withColumn("locality",F.initcap(F.col("locality")))

# COMMAND ----------

write_to_silver(
    df = circuits_final_df, 
    target_table = silver_table, 
    merge_condition = "t.circuit_id = s.circuit_id",
    columns_to_update = [
        "circuit_name", 
        "country",
        "latitude",
        "longitude", 
        "locality",
        "ingestion_timestamp",
        "source_file",
        "batch_id"]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.silver.circuits