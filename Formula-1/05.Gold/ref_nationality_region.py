# Databricks notebook source
# Databricks notebook source
 # Build Nationality Region Reference

#  1. Create a dataframe with list of nationalities and corresponding geographic regions
#  1. Write the dataframe to gold `ref_nationality_region` table

# COMMAND ----------

# MAGIC %run ../00.Common/01.Configuration

# COMMAND ----------

target_table = f"{catalog_name}.{gold_schema}.ref_nationality_region"

from pyspark.sql import functions as F

from pyspark.sql import Row


# COMMAND ----------

# Manually curated nationality → region mapping
nationality_region_map_rows = [
    # Europe
    Row(nationality="British",           region="Europe"),
    Row(nationality="Italian",           region="Europe"),
    Row(nationality="French",            region="Europe"),
    Row(nationality="German",            region="Europe"),
    Row(nationality="Swiss",             region="Europe"),
    Row(nationality="Dutch",             region="Europe"),
    Row(nationality="Belgium",           region="Europe"),
    Row(nationality="Belgian",           region="Europe"),
    Row(nationality="Irish",             region="Europe"),
    Row(nationality="Spanish",           region="Europe"),
    Row(nationality="Austrian",          region="Europe"),
    Row(nationality="East German",       region="Europe"),
    Row(nationality="Russian",           region="Europe"),
    Row(nationality="Finnish",           region="Europe"),
    Row(nationality="Polish",            region="Europe"),
    Row(nationality="Portuguese",        region="Europe"),
    Row(nationality="Hungarian",         region="Europe"),
    Row(nationality="Danish",            region="Europe"),
    Row(nationality="Czech",             region="Europe"),
    Row(nationality="Liechtensteiner",   region="Europe"),
    Row(nationality="Monegasque",        region="Europe"),
    Row(nationality="Swedish",           region="Europe"),
    Row(nationality="Argentine-italian", region="Europe"),
    Row(nationality="American-italian",  region="Europe"),

    # North America
    Row(nationality="American",          region="North America"),
    Row(nationality="Canadian",          region="North America"),
    Row(nationality="Mexican",           region="North America"),

    # South America
    Row(nationality="Brazilian",         region="South America"),
    Row(nationality="Chilean",           region="South America"),
    Row(nationality="Argentine",         region="South America"),
    Row(nationality="Uruguayan",         region="South America"),
    Row(nationality="Venezuelan",        region="South America"),
    Row(nationality="Colombian",         region="South America"),

    # Africa
    Row(nationality="South African",     region="Africa"),
    Row(nationality="Rhodesian",         region="Africa"),

    # Asia
    Row(nationality="Indian",            region="Asia"),
    Row(nationality="Chinese",           region="Asia"),
    Row(nationality="Japanese",          region="Asia"),
    Row(nationality="Malaysian",         region="Asia"),
    Row(nationality="Hong Kong",         region="Asia"),
    Row(nationality="Indonesian",        region="Asia"),
    Row(nationality="Thai",              region="Asia"),

    # Oceania
    Row(nationality="Australian",        region="Oceania"),
    Row(nationality="New Zealand",       region="Oceania"),
    Row(nationality="New Zealander",     region="Oceania"),
]

ref_nationality_region_df = spark.createDataFrame(nationality_region_map_rows)



# COMMAND ----------

 #### Step 2 - Write the dataframe to the `gold` `ref_nationality_region` table

# COMMAND ----------

(
    ref_nationality_region_df
        .write
        .format("delta")
        .mode("overwrite")             
        .saveAsTable(target_table)
)

# COMMAND ----------

display(spark.table(target_table))

# COMMAND ----------

