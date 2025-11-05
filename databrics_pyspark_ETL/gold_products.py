# Databricks notebook source
# MAGIC %md
# MAGIC ### Delta Live Table

# COMMAND ----------

import dlt
from pyspark.sql.functions import *

# COMMAND ----------

# MAGIC %md
# MAGIC Streaming Table

# COMMAND ----------

# Expectations

my_rules = {
    "rule1": "product_id IS NOT NULL",
    "rule2": "product_name IS NOT NULL"
}

# COMMAND ----------

@dlt.table()
@dlt.expect_all_or_drop(my_rules)

def dim_products_stage():
  
  df = spark.readStream.table("bharath_cata.silver.products")

  return df

# COMMAND ----------

# MAGIC %md
# MAGIC Delta view

# COMMAND ----------

@dlt.view()

def dim_products_view():

    df = spark.readStream.table("Live.dim_products_stage")

    return df

# COMMAND ----------

# MAGIC %md
# MAGIC dim_products

# COMMAND ----------

dlt.create_streaming_table("dim_products")

# COMMAND ----------

dlt.apply_changes(
    target = "dim_products",
    source = "Live.dim_products_view",
    keys = "product_id",
    sequence_by = "product_id",
    stored_as_scd_type = 2
)