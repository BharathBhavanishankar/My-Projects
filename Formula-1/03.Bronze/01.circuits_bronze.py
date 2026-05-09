# Databricks notebook source
dbutils.widgets.text('p_batch_id','')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/02.bronze_helper

# COMMAND ----------

v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

circuits_schema = StructType([
    StructField('circuitId', StringType(), True),
    StructField('url', StringType(), True),
    StructField('circuitName', StringType(), True),
    StructField('lat', DoubleType(), True),
    StructField('long', DoubleType(), True),
    StructField('locality', StringType(), True),
    StructField('country', StringType(), True)
])

# COMMAND ----------

source_file = f"{landing_folder_path}/{v_batch_id}/circuits.csv"
table_name = f"{catalog_name}.{bronze_schema}.circuits"

# COMMAND ----------

circuits_df = (
    spark.read
         .format('csv')
         .option('header', 'true')
         .option('mode','FAILFAST')
         .schema(circuits_schema)
         .load(source_file)
)

# COMMAND ----------

circuits_final_df = add_metadata(circuits_df)

# COMMAND ----------

# writing the data

# circuits_final_df.write
#     .mode('overwrite')
#     .format('delta')
#     .partitionBy('batch_id')
#     .option('replaceWhere',f"batch_id = {v_batch_id}")
#     .saveAsTable(table_name)

# COMMAND ----------

bronze_update(target_table=table_name, batch_id=v_batch_id, df=circuits_final_df)