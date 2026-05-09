# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/03.silver_helper

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

bronze_table = f"{catalog_name}.{bronze_schema}.races"
silver_table = f"{catalog_name}.{silver_schema}.races"

# COMMAND ----------

races_df = spark.read.table(bronze_table).filter(F.col('batch_id') == v_batch_id)

# COMMAND ----------

races_selected_df = races_df.select("season","round","raceName","date","circuitID","ingestion_timestamp","source_file","batch_id")

# COMMAND ----------

races_renamed_df = races_selected_df.withColumnsRenamed({"raceName":"race_name","circuitID":"circuit_id", "date":"race_date"})

# COMMAND ----------

races_nonull_df = races_renamed_df.filter(F.col("season").isNotNull() & F.col("round").isNotNull())

# COMMAND ----------

races_validated_df = races_nonull_df.dropDuplicates()

# COMMAND ----------

races_final_df = races_validated_df.withColumn("race_name",F.initcap(F.col("race_name")))

# COMMAND ----------

write_to_silver(
  df = races_final_df,
  target_table = silver_table,
  merge_condition = 
    "s.season = t.season AND s.round = t.round",
  columns_to_update = 
    [
      "race_name",
      "race_date",
      "ingestion_timestamp",
      "source_file",
      "batch_id"
    ]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.silver.races

# COMMAND ----------

