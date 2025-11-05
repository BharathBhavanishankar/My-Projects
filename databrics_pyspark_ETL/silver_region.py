# Databricks notebook source
df = spark.read.table("bharath_cata.bronze.regions")

# COMMAND ----------

df.display()

# COMMAND ----------

df = df.drop("_rescued_data")

# COMMAND ----------

df.display()

# COMMAND ----------

df.write.format("delta").mode("overwrite").save("abfss://silver@bharathetlproject.dfs.core.windows.net/regions")

# COMMAND ----------

spark.read.format("delta").load("abfss://silver@bharathetlproject.dfs.core.windows.net/products").display()

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists bharath_cata.silver.regions
# MAGIC using delta
# MAGIC location "abfss://silver@bharathetlproject.dfs.core.windows.net/regions"

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bharath_cata.silver.regions

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS bharath_cata.silver.region;

# COMMAND ----------

