# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "8ab995a9-82ae-4bab-8785-781ab1dc5f36",
# META       "default_lakehouse_name": "Banking_Credit_Data",
# META       "default_lakehouse_workspace_id": "1beb3139-2c5d-4cb3-b416-c46404555b49",
# META       "known_lakehouses": [
# META         {
# META           "id": "8ab995a9-82ae-4bab-8785-781ab1dc5f36"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Load Banking Data

# CELL ********************

from pyspark.sql import functions as F

files = {
    "Customers": "Files/customers.csv",
    "CreditProfiles": "Files/credit_profiles.csv",
    "Loans": "Files/loans.csv",
    "Payments": "Files/payments.csv",
    "Transactions": "Files/transactions.csv",
}

for table_name, path in files.items():
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(path)
    )

    df.write.mode("overwrite").format("delta").saveAsTable(table_name)

    print(f"Created {table_name}: {df.count()} rows")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Add FullName
from pyspark.sql import functions as F

df = spark.sql("SELECT * FROM Banking_Credit_Data.dbo.Customers")
df_enriched = df.withColumn("FullName", F.concat_ws(" ", F.col("FirstName"), F.col("LastName")))
#display(df_enriched)

df_enriched.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteschema","true")\
    .saveAsTable("Banking_Credit_Data.dbo.Customers")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
