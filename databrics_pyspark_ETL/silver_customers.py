# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %md
# MAGIC **Data Reading**

# COMMAND ----------

df = spark.read.format("parquet").load("abfss://bronze@bharathetlproject.dfs.core.windows.net/customers")

# COMMAND ----------

df.display()

# COMMAND ----------

df = df.drop("_rescued_data")

# COMMAND ----------

df = df.withColumn("domain",split(col("email"),"@")[1])

# COMMAND ----------

df.display()

# COMMAND ----------

df.groupBy("domain").agg(countDistinct("customer_id").alias("total_customers")).sort("total_customers",ascending=False).display()

# COMMAND ----------

df = df.withColumn("full_name",concat(col("first_name"),lit(" "),col("last_name")))

# COMMAND ----------

df = df.drop("first_name","last_name")

# COMMAND ----------

df.display()

# COMMAND ----------

df.write.format("delta").mode("overwrite").save("abfss://silver@bharathetlproject.dfs.core.windows.net/customers")

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists bharath_cata.silver.customers
# MAGIC using delta
# MAGIC location "abfss://silver@bharathetlproject.dfs.core.windows.net/customers"

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bharath_cata.silver.customers

# COMMAND ----------

