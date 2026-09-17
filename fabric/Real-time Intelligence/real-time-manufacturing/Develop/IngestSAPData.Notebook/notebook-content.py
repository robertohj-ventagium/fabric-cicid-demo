# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "338844e9-6b87-4aa2-b0bd-bc584da8e6fd",
# META       "default_lakehouse_name": "ManufacturingData",
# META       "default_lakehouse_workspace_id": "1beb3139-2c5d-4cb3-b416-c46404555b49",
# META       "known_lakehouses": [
# META         {
# META           "id": "338844e9-6b87-4aa2-b0bd-bc584da8e6fd"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

ws_id = notebookutils.runtime.context["currentWorkspaceId"]
manu_lh = "338844e9-6b87-4aa2-b0bd-bc584da8e6fd"
manu_data = notebookutils.lakehouse.getWithProperties(manu_lh).properties["abfsPath"]
target = f"{manu_data}/Tables/landing_sap"
source = f"{manu_data}/Files/data"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

tables = ['I_ADDRESS',
 'I_CUSTOMER',
 'I_EQUIPMENT',
 'I_EQUIPMENTTEXT',
 'I_PLANT',
 'I_PRODUCT',
 'I_PRODUCTDESCRIPTION',
 'I_SUPPLIER']

print("🚀 Ingesting SAP Data")

for t in tables:
    df = spark.read.format("parquet").load(f"{source}/{t}")
    df.write.mode("overwrite").format("delta").save(f"{target}/{t}")
    print(f"✅ Written table: {t}")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
