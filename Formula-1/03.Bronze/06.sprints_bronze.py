# Databricks notebook source
dbutils.widgets.text('p_batch_id','')
v_batch_id = dbutils.widgets.get('p_batch_id')

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

# MAGIC %run ../00.Common/02.bronze_helper

# COMMAND ----------

sprints_schema = 'constructorId STRING,date DATE,driverId STRING,grid INT,laps INT,number INT,points DECIMAL(3,1),position INT,positionText STRING,raceName STRING,round INT,season STRING,status STRING,url STRING'

# COMMAND ----------

source_file = f"{landing_folder_path}/{v_batch_id}/sprints"
table_name = f"{catalog_name}.{bronze_schema}.sprints"

# COMMAND ----------

sprints_df = (
    spark.read
    .format('json')
    .option('multiLine','true')
    .option('header','true')
    .schema(sprints_schema)
    .option('mode','FASTFAIL')
    .load(source_file)
)

# COMMAND ----------

sprints_final_df = add_metadata(sprints_df)

# COMMAND ----------

bronze_update(df = sprints_final_df, target_table = table_name, batch_id = v_batch_id)