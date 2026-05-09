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

bronze_table = f"{catalog_name}.{bronze_schema}.constructors"
silver_table = f"{catalog_name}.{silver_schema}.constructors"

# COMMAND ----------

constructors_df = spark.read.table(bronze_table).filter(F.col("batch_id") == v_batch_id)

# COMMAND ----------

constructors_selected_df = constructors_df.select("constructorId","name","nationality","ingestion_timestamp","source_file","batch_id")

# COMMAND ----------

constructors_renamed_df = constructors_selected_df.withColumnsRenamed({"constructorId":"constructor_id","name":"constructor_name"})


# COMMAND ----------

constructors_nonull_df = constructors_renamed_df.filter(F.col("constructor_id").isNotNull())

# COMMAND ----------

constructors_validated_df = constructors_nonull_df.dropDuplicates()

# COMMAND ----------

constructors_final_df = constructors_validated_df.withColumn("nationality",F.initcap(F.col("nationality")))

# COMMAND ----------

write_to_silver(
  df = constructors_final_df,
  target_table = silver_table,
  merge_condition = "s.constructor_id = t.constructor_id",
  columns_to_update = 
    ["constructor_name",
     "nationality",
     "ingestion_timestamp",
     "source_file",
     "batch_id"]
)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.silver.constructors