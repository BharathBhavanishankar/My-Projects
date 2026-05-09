# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS databricks_course_ext_loc_formula1incr
# MAGIC     URL 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/'
# MAGIC     WITH (STORAGE CREDENTIAL `databricks_course_sc`)
# MAGIC     COMMENT 'external location for the formula1incr container';

# COMMAND ----------

