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

bronze_table = f"{catalog_name}.{bronze_schema}.drivers"
silver_table = f"{catalog_name}.{silver_schema}.drivers"

# COMMAND ----------

drivers_df = spark.read.table(bronze_table).filter(F.col("batch_id") == v_batch_id)

# COMMAND ----------

drivers_selected_df = drivers_df.drop("url")

# COMMAND ----------

drivers_renamed_df = drivers_selected_df.withColumnsRenamed({"dateOfBirth":"date_of_birth","driverId":"driver_id"})


# COMMAND ----------

drivers_nonull_df = drivers_renamed_df.filter(F.col("driver_id").isNotNull())

# COMMAND ----------

drivers_validated_df = drivers_nonull_df .dropDuplicates()

# COMMAND ----------

drivers_concatenated_df = drivers_validated_df.withColumn("driver_name",F.concat_ws(" ",F.col("name.givenName"), F.col("name.familyName")))

# COMMAND ----------

drivers_final_df = drivers_concatenated_df.withColumn("nationality",F.initcap(F.col("nationality"))) \
.withColumn("driver_name",F.initcap(F.col("driver_name")))

# COMMAND ----------

drivers_final_df = drivers_final_df.drop("name")

# COMMAND ----------

write_to_silver(
    df = drivers_final_df,
    target_table = silver_table,
    merge_condition = "t.driver_id = s.driver_id",
    columns_to_update = 
    ["date_of_birth",
     "nationality",
     "driver_name",
     "ingestion_timestamp",
     "source_file","batch_id"]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.silver.drivers