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

bronze_table = f"{catalog_name}.{bronze_schema}.sprints"
silver_table = f"{catalog_name}.{silver_schema}.sprints"

# COMMAND ----------

sprints_df = spark.read.table(bronze_table).filter(F.col("batch_id") == v_batch_id)

# COMMAND ----------

sprints_selected_df = sprints_df.drop("url")

# COMMAND ----------

sprints_renamed_df = sprints_selected_df.withColumnsRenamed({"constructorId":"constructor_id","driverId":"driver_id","raceName":"race_name","laps":"completed_laps","number":"car_number","position":"finish_position","date":"race_date","grid":"grid_position","positionText":"finish_position_text"})

# COMMAND ----------

sprints_nonull_df = sprints_renamed_df.filter((F.col("season").isNotNull()) & (F.col("round").isNotNull()) & (F.col("constructor_id").isNotNull()) & (F.col("driver_id").isNotNull()))

# COMMAND ----------

sprints_validated_df = sprints_nonull_df.dropDuplicates(["season", "round", "constructor_id", "driver_id"])

# COMMAND ----------

sprints_final_df = sprints_validated_df.withColumn("race_name",F.initcap(F.col("race_name")))

# COMMAND ----------

write_to_silver(
  df = sprints_final_df,
  target_table = silver_table,
  merge_condition= 
  "t.season = s.season AND t.round = s.round AND t.constructor_id = s.constructor_id AND t.driver_id = s.driver_id",
  columns_to_update = 
    [ "race_date",
      "grid_position",
      "race_name",
      "completed_laps",
      "car_number",
      "finish_position",
      "finish_position_text",
      "status",
      "points",
      "ingestion_timestamp",
      "source_file",
      "batch_id"]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.silver.sprints