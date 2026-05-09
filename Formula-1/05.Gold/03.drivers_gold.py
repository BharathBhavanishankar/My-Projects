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

source_table = f"{catalog_name}.{silver_schema}.drivers"
nr_table = f"{catalog_name}.{gold_schema}.ref_nationality_region"
gold_table = f"{catalog_name}.{gold_schema}.dim_drivers"

# COMMAND ----------

drivers_df = spark.read.table(source_table).filter(F.col('batch_id') == v_batch_id)
nr_df = spark.read.table(nr_table)

# COMMAND ----------

# DBTITLE 1,Fix join syntax for driver nationality
drivers_nr_df = drivers_df.alias("d").join(nr_df.alias("n"), F.col("d.nationality") == F.col("n.nationality"), "inner")

# COMMAND ----------

drivers_nr_df = drivers_nr_df.select('d.date_of_birth','d.driver_id','d.driver_name','d.nationality','d.created_timestamp','d.updated_timestamp','n.region')

# COMMAND ----------

write_to_gold(
    df = drivers_nr_df,
    target_table = gold_table,
    merge_condition = "t.driver_id = s.driver_id",
    columns_to_update = 
    [
        "driver_name",
        "date_of_birth",
        "nationality",
        "region"
    ]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.gold.dim_drivers;