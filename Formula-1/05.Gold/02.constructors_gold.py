# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/04.gold_helper

# COMMAND ----------

source_table = f"{catalog_name}.{silver_schema}.constructors"
nr_table = f"{catalog_name}.{gold_schema}.ref_nationality_region"
gold_table = f"{catalog_name}.{gold_schema}.dim_constructors"

# COMMAND ----------

constructors_df = spark.read.table(source_table).filter(F.col('batch_id') == v_batch_id)
nr_df = spark.read.table(nr_table)

# COMMAND ----------

constructors_nr_df = constructors_df.alias('c').join(nr_df.alias('n'),F.col('c.nationality') == F.col('n.nationality'),how = 'left')

# COMMAND ----------

constructors_nr_final_df = constructors_nr_df.select('c.constructor_id','c.constructor_name','c.nationality','n.region')

# COMMAND ----------

constructors_nr_final_df.columns

# COMMAND ----------

write_to_gold(
              df = constructors_nr_final_df,
              target_table = gold_table,
              merge_condition = "t.constructor_id = s.constructor_id",
              columns_to_update = 
              [
                  "constructor_name",
                  "nationality",
                  "region"
              ]
              )

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from formula1incr.gold.dim_constructors;