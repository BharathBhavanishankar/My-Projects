# Databricks notebook source
dbutils.widgets.text("file_name","")

# COMMAND ----------

p_file_name = dbutils.widgets.get("file_name")

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Data Reading**

# COMMAND ----------

df = spark.readStream.format("cloudFiles")\
                .option("cloudFiles.format", "parquet")\
                .option("cloudFiles.SchemaLocation",f"abfss://bronze@bharathetlproject.dfs.core.windows.net/checkpoint_{p_file_name}")\
                .load(f"abfss://source@bharathetlproject.dfs.core.windows.net/{p_file_name}")
                #1st line: when autoloader is required then cloudfiles should be used
                #3rd line: schema location is declared within checkpoint_orders folder
                #4th line: source location is declared

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Data Writing**

# COMMAND ----------

df.writeStream.format("parquet")\
              .outputMode("append")\
              .option("checkpointLocation", f"abfss://bronze@bharathetlproject.dfs.core.windows.net/checkpoint_{p_file_name}")\
              .option("path",f"abfss://bronze@bharathetlproject.dfs.core.windows.net/{p_file_name}")\
              .trigger(once=True)\
              .start()