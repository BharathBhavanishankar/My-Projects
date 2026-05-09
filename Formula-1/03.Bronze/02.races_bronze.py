# Databricks notebook source
# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/02.bronze_helper

# COMMAND ----------

dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

source_file = f"{landing_folder_path}/{v_batch_id}/races.csv"
table_name = f"{catalog_name}.{bronze_schema}.races"

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

races_schema = StructType(fields=[StructField("season", IntegerType(), True),
                                  StructField("round", IntegerType(), True),
                                  StructField("url", StringType(), True),
                                  StructField("raceName", StringType(), True),
                                  StructField("date", DateType(), True),
                                  StructField("circuitID", StringType(), True)])

# COMMAND ----------

races_df = (
spark.read
    .format('csv')
    .option('header','true')
    .schema(races_schema)
    .option('mode','FASTFAIL')
    .load(source_file)
)

# COMMAND ----------

# adding metadata
# from pyspark.sql.functions import current_timestamp, col

races_final_df = add_metadata(races_df)

# COMMAND ----------

bronze_update(df = races_final_df, target_table = table_name, batch_id = v_batch_id)