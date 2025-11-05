# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df = spark.read.format("parquet").load("abfss://bronze@bharathetlproject.dfs.core.windows.net/products")

# COMMAND ----------

df.display()

# COMMAND ----------

df = df.drop("_rescued_data")

# COMMAND ----------

df.display()

# COMMAND ----------

df.createOrReplaceTempView("products")

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Functions**

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace function bharath_cata.bronze.discount_fun(p_price double)
# MAGIC returns double
# MAGIC language sql
# MAGIC return p_price * 0.90

# COMMAND ----------

# MAGIC %sql
# MAGIC select product_id, price, round(bharath_cata.bronze.discount_fun(price),2) as discounted_price
# MAGIC from products;

# COMMAND ----------

df = df.withColumn("discounted_price", expr("bharath_cata.bronze.discount_fun(price)"))

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace function bharath_cata.bronze.upper_fun(p_brand string)
# MAGIC returns string
# MAGIC language python
# MAGIC as
# MAGIC $$
# MAGIC     return p_brand.upper()
# MAGIC $$

# COMMAND ----------

# MAGIC %sql
# MAGIC select product_id, brand, bharath_cata.bronze.upper_fun(brand) as brand_upper
# MAGIC from products

# COMMAND ----------

df.write.format("delta").mode("overwrite").save("abfss://silver@bharathetlproject.dfs.core.windows.net/products")

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists bharath_cata.silver.products
# MAGIC using delta
# MAGIC location "abfss://silver@bharathetlproject.dfs.core.windows.net/products"

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bharath_cata.silver.products

# COMMAND ----------

