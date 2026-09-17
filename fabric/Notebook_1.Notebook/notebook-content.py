# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0ebf15be-7a9f-468a-9974-686ae4f97195",
# META       "default_lakehouse_name": "Bronze_Lakehouse",
# META       "default_lakehouse_workspace_id": "06e08957-0a0e-4419-a9d1-219c95cf4b2c",
# META       "known_lakehouses": [
# META         {
# META           "id": "0ebf15be-7a9f-468a-9974-686ae4f97195"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

df   = spark \
    .read \
    .format("delta") \
    .load("abfss://01_Bronze@onelake.dfs.fabric.microsoft.com/Bronze_Lakehouse.Lakehouse/Tables/Fabric_Report_Pages")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(spark.sql("describe history {df}",df=df))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
