# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/02.bronze_helper

# COMMAND ----------

source_file = f"{landing_folder_path}/{v_batch_id}/constructors.json"
table_name = f"{catalog_name}.{bronze_schema}.constructors"

# COMMAND ----------

constructors_schema = 'constructorId STRING, name STRING, nationality STRING, url STRING'

# COMMAND ----------

consturctors_df = (spark.read
                   .format('json')
                   .option('header','true')
                   .option('mode','FAILFAST')
                   .schema(constructors_schema)
                   .load(source_file)
                   )

# COMMAND ----------

constructors_final_df = add_metadata(consturctors_df)

# COMMAND ----------

bronze_update(df = constructors_final_df, target_table = table_name, batch_id = v_batch_id)