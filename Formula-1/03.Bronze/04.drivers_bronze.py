# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/02.bronze_helper

# COMMAND ----------

source_file = f"{landing_folder_path}/{v_batch_id}/drivers.json"
table_name = f"{catalog_name}.{bronze_schema}.drivers"

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

name_schema = StructType(
    [StructField('givenName', StringType()),
     StructField('familyName', StringType())
     ]
)

drivers_schema = StructType(
    [StructField('dateOfBirth', DateType()),
     StructField('driverId', StringType()),
     StructField('name', name_schema),
     StructField('nationality', StringType()),
     StructField('url', StringType())
     ]
)


# COMMAND ----------

drivers_df = (
    spark.read
    .format('json')
    .option('header','true')
    .option('mode','FASTFAIL')
    .schema(drivers_schema)
    .load(source_file)
)

# COMMAND ----------

drivers_final_df = add_metadata(drivers_df)

# COMMAND ----------

bronze_update(df = drivers_final_df, target_table = table_name, batch_id = v_batch_id)