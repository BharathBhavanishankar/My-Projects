# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/04.gold_helper

# COMMAND ----------

target_table = f"{catalog_name}.{gold_schema}.dim_races"
   

# COMMAND ----------

races_df = spark.read.table(f"{catalog_name}.{silver_schema}.races").filter(F.col("batch_id") == v_batch_id)

# COMMAND ----------

circuits_df = (
                spark.read.table(f"{catalog_name}.{silver_schema}.circuits")
                         .filter(F.col("batch_id") == v_batch_id)
)

# COMMAND ----------

races_circuits_final_df = (
races_df.alias("r").join(circuits_df.alias("c"), F.col("r.circuit_id") == F.col("c.circuit_id"), how='inner')
.select('r.season','r.round','r.race_name','r.race_date','c.circuit_name','c.locality','c.country')
)

# COMMAND ----------

write_to_gold(
    df = races_circuits_final_df,
    target_table = target_table,
    merge_condition = "t.season = s.season AND t.round = s.round",
    columns_to_update = 
        [
            "race_name",
            "race_date",
            "circuit_name",
            "locality",
            "country"
        ]
)

# COMMAND ----------

display(spark.read.table(target_table))