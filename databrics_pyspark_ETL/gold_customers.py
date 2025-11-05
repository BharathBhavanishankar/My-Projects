# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

init_load_flag = int(dbutils.widgets.get("init_load_flag"))

# COMMAND ----------

# MAGIC %md
# MAGIC **Data reading**

# COMMAND ----------

df = spark.sql("select * from bharath_cata.silver.customers")

# COMMAND ----------

df = df.dropDuplicates(subset=["customer_id"])

# COMMAND ----------

# MAGIC %md
# MAGIC **Dividing Old vs New records**

# COMMAND ----------

if init_load_flag == 0:
    df_old = spark.sql("select dimcustomerkey, customer_id, created_date, updated_date from bharath_cata.gold.dim_customers")

else:
    df_old = spark.sql("select 0 dimcustomerkey, 0 customer_id, 0 created_date, 0 updated_date from bharath_cata.silver.customers where 1=0")

# COMMAND ----------

# MAGIC %md
# MAGIC **Renaming columns of old df**

# COMMAND ----------

df_old = df_old.withColumnRenamed("dimcustomerkey","old_dimcustomerkey")\
      .withColumnRenamed("customer_id","old_customer_id")\
      .withColumnRenamed("created_date","old_created_date")\
      .withColumnRenamed("updated_date","old_updated_date")

# COMMAND ----------

# MAGIC %md
# MAGIC **Dataframe Join**

# COMMAND ----------

df_join = df.join(df_old, df.customer_id == df_old.old_customer_id, "left")

# COMMAND ----------

df_join.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **Separating New vs Old**

# COMMAND ----------

df_new = df_join.filter(df_join["old_dimcustomerkey"].isNull())

# COMMAND ----------

df_old = df_join.filter(df_join["old_dimcustomerkey"].isNotNull())

# COMMAND ----------

# MAGIC %md
# MAGIC **Preparing df_old**

# COMMAND ----------

# dropping all the columns which are not required

df_old = df_old.drop("old_customer_id","old_updated_date")

# renaming old_dimcustomerkey to dimcustomerkey

df_old = df_old.withColumnRenamed("old_dimcustomerkey","dimcustomerkey") 

# renaming old_created_date to created_date

df_old = df_old.withColumnRenamed("old_created_date","create_date")

# converting create_date datatype

df_old = df_old.withColumn("create_date",to_timestamp(col("create_date")))

# updating the update_date with current timestamp

df_old = df_old.withColumn("update_date",current_timestamp())

# COMMAND ----------

df_old.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **preparing df_new**

# COMMAND ----------

df_new.limit(5).display()

# COMMAND ----------

# dropping all the columns which are not required

df_new = df_new.drop("old_customer_id","old_dimcustomerkey","old_updated_date","old_created_date")

# adding new column create date to df_new

df_new = df_new.withColumn("create_date",current_timestamp())

# adding new column update date to df_new

df_new = df_new.withColumn("update_date", current_timestamp())

# COMMAND ----------

df_old.columns

# COMMAND ----------

df_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC surrogate key - form 1

# COMMAND ----------

df_new = df_new.withColumn("dimcustomerkey",monotonically_increasing_id()+lit(1)).orderBy("dimcustomerkey",ascending=True)

# COMMAND ----------

df_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC **Adding max surrogate key**

# COMMAND ----------

if init_load_flag == 1:
    max_surrogate_key = 0
else:
    df_maxsur = spark.sql("select max(dimcustomerkey) as max_surrogate_key from bharath_cata.gold.customers")

    #coverting df_maxsur to max_surrogate_key
    max_surrogate_key = df_maxsur.collect()[0]['max_surrogate_key']

# COMMAND ----------

df_new = df_new.withColumn("dimcustomerkey",lit(max_surrogate_key)+col("dimcustomerkey"))

# COMMAND ----------

# MAGIC %md
# MAGIC **union of df_new & df_old**

# COMMAND ----------

df_final = df_old.unionByName(df_new)

# COMMAND ----------

df_final.display()

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

if spark.catalog.tableExists("bharath_cata.gold.dim_customers"):
    dlt_obj = DeltaTable.forPath(spark,"abfss://gold@bharathetlproject.dfs.core.windows.net/dim_customers")
    dlt_obj.alias("trg").merge(df_final.alias("src"),"trg.dimcustomerkey = src.dimcustomerkey").whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

else:
    df_final.write.mode("overwrite")\
    .option("path","abfss://gold@bharathetlproject.dfs.core.windows.net/dim_customers")\
    .saveAsTable("bharath_cata.gold.dim_customers")

# COMMAND ----------

