# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Data Reading**

# COMMAND ----------

df = spark.read.format("parquet").load("abfss://bronze@bharathetlproject.dfs.core.windows.net/orders")

# COMMAND ----------

df.columns

# COMMAND ----------

df = df.withColumn("year", year(df.order_date))

# COMMAND ----------

df1 = df

# COMMAND ----------

df1.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Window OOP

# COMMAND ----------

class windows:

    def dense_rank(self, df):
        df_dense_rank = df.withColumn("dense_rank",dense_rank().over(Window.partitionBy("year").orderBy(desc("total_amount"))))
        return df_dense_rank
    
    def rank(self, df):
        df_rank = df.withColumn("rank",rank().over(Window.partitionBy("year").orderBy(desc("total_amount"))))
        return df_rank
    
    def row_number(self, df):
        df_row_number = df.withColumn("row_number",row_number().over(Window.partitionBy("year").orderBy(desc("total_amount"))))
        return df_row_number

# COMMAND ----------

obj = windows()

# COMMAND ----------

df1 = obj.dense_rank(df1)
df1 = obj.rank(df1)
df1 = obj.row_number(df1)

# COMMAND ----------

df1.display()

# COMMAND ----------

df1.printSchema()

# COMMAND ----------

df1 = df1.drop("_rescued_data").drop("dense_rank").drop("row_number").drop("rank")

# COMMAND ----------

df1 = df1.withColumn("order_date",to_timestamp(col("order_date")))

# COMMAND ----------

df1.write.format("delta").mode("overwrite").save("abfss://silver@bharathetlproject.dfs.core.windows.net/orders")

# COMMAND ----------

df1.printSchema()

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists bharath_cata.silver.orders
# MAGIC using delta
# MAGIC location "abfss://silver@bharathetlproject.dfs.core.windows.net/orders"

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bharath_cata.silver.orders

# COMMAND ----------

