# Databricks notebook source
# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS formula1incr
# MAGIC MANAGED LOCATION 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/'
# MAGIC COMMENT 'formula1incr catalog for the unity catalog > project formula1incr';

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CREATING SCHEMA
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1incr.landing;
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1incr.bronze
# MAGIC     MANAGED LOCATION 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/bronze';
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1incr.silver
# MAGIC     MANAGED LOCATION 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/silver';
# MAGIC CREATE SCHEMA IF NOT EXISTS formula1incr.gold
# MAGIC     MANAGED LOCATION 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/gold';

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG formula1incr;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS;

# COMMAND ----------

# MAGIC %fs ls 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/landing'

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC --CREATING EXTERNAL VOLUME
# MAGIC
# MAGIC CREATE EXTERNAL VOLUME formula1incr.landing.files
# MAGIC LOCATION 'abfss://formula1incr@databricksstorage96.dfs.core.windows.net/landing';

# COMMAND ----------



# COMMAND ----------

