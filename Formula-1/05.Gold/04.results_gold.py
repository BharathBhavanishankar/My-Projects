# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/04.gold_helper

# COMMAND ----------

target_table = f"{catalog_name}.{gold_schema}.fact_session_results"

from pyspark.sql import functions as F


results_df = (
    spark.table(f"{catalog_name}.{silver_schema}.results")
         .withColumn("session_type", F.lit("RACE"))
         .drop("race_name", "race_date", "ingestion_timestamp", "source_file","created_timestamp","updated_timestamp")
         .filter(F.col("batch_id") == v_batch_id)
)


sprints_df = (
    spark.table(f"{catalog_name}.{silver_schema}.sprints")
         .withColumn("session_type", F.lit("SPRINT"))
         .drop("race_name", "race_date", "ingestion_timestamp", "source_file","created_timestamp","updated_timestamp")
         .filter(F.col("batch_id") == v_batch_id)
)


results_sprints_df = results_df.unionByName(sprints_df)

results_sprints_df = results_sprints_df.withColumnsRenamed({'finish_position': 'final_position','finish_position_text': 'final_position_text'})


fact_session_results_df = (
    results_sprints_df
        .withColumn("is_win", (F.col("final_position") == 1).cast('int'))
        .withColumn("is_podium", (F.col("final_position").between(1, 3)).cast('int'))
        .withColumn("has_points", (F.col("points") > 0).cast('int'))
)

fact_session_results_df = fact_session_results_df.select('constructor_id','driver_id','season','round','session_type','grid_position','completed_laps','car_number','points','final_position','final_position_text','status','is_win','is_podium','has_points')

# COMMAND ----------

fact_session_results_df = fact_session_results_df.dropDuplicates(["season","round","session_type","constructor_id","driver_id"])

# COMMAND ----------

write_to_gold(
    df = fact_session_results_df,
    target_table = target_table,
    merge_condition = """t.season = s.season AND t.round = s.round AND t.session_type = s.session_type AND t.constructor_id = s.constructor_id AND t.driver_id = s.driver_id""",
    columns_to_update = 
    [
        "grid_position",
        "completed_laps",
        "car_number",
        "points",
        "final_position",
        "final_position_text",
        "status",
        "is_win",
        "is_podium",
        "has_points"
    ]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.gold.fact_session_results;