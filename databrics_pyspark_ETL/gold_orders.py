# Databricks notebook source
# MAGIC %md
# MAGIC ### Fact orders

# COMMAND ----------

# MAGIC %md
# MAGIC Data reading

# COMMAND ----------

df = spark.sql("select * from bharath_cata.silver.orders")
df.display()

# COMMAND ----------

df_cus = spark.sql("select dimcustomerkey, customer_id as dim_cust from bharath_cata.gold.dim_customers")
df_pdt = spark.sql("select product_id as dimproductkey, product_id as dim_pro from bharath_cata.gold.dim_products")

# COMMAND ----------

df_pdt.display()

# COMMAND ----------

df_fact = df.join(df_cus, df["customer_id"] == df_cus["dim_cust"], how = "left").join(df_pdt, df["product_id"] == df_pdt["dim_pro"], how = "left")
df_fact_new = df_fact.drop("dim_cust", "dim_pro","customer_id","product_id")

# COMMAND ----------

df_fact_new.display()

# COMMAND ----------

# MAGIC %md
# MAGIC UPSERT on fact table

# COMMAND ----------

from delta.tables import DeltaTable

# COMMAND ----------

if spark.catalog.tableExists("bharath_cata.gold.fact_orders"):
  dlt_obj = DeltaTable.forName(spark,"bharath_cata.gold.fact_orders")
  dlt_obj.alias("trg").merge(df_fact_new.alias("src"),"trg.order_id = src.order_id AND trg.dimcustomerkey = src.dimcustomerkey AND trg.dimproductkey = src.dimproductkey")\
  .whenMatchedUpdateAll()\
  .whenNotMatchedInsertAll()\
  .execute()
else:
  df_fact_new.write.format("delta")\
  .option("path","abfss://gold@bharathetlproject.dfs.core.windows.net/fact_orders")\
  .saveAsTable("bharath_cata.gold.fact_orders")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from bharath_cata.gold.fact_orders

# COMMAND ----------

