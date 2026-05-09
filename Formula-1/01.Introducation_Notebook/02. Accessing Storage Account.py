# Databricks notebook source
# MAGIC %md
# MAGIC %fs ls 'abfss://container_name@storage_name.dfs.core.windows.net/'

# COMMAND ----------

# MAGIC %fs ls 'abfss://demo@databricksstorage96.dfs.core.windows.net/'

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS databricks_course_ext_loc_demo
# MAGIC     URL 'abfss://demo@databricksstorage96.dfs.core.windows.net/'
# MAGIC     WITH (STORAGE CREDENTIAL `databricks_course_sc`)
# MAGIC     COMMENT 'external location for the demo container';