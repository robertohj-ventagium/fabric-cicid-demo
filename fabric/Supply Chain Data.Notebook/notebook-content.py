# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "eb342914-631b-4005-bfe1-b37604c8d00b",
# META       "default_lakehouse_name": "OmniRoute_Lakehouse",
# META       "default_lakehouse_workspace_id": "904870c3-1d7b-491b-be30-5fe1782f818f",
# META       "known_lakehouses": [
# META         {
# META           "id": "eb342914-631b-4005-bfe1-b37604c8d00b"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Supply Chain Data Generation  
# This Notebook generates realistic data based on environment specific settings.

# MARKDOWN ********************

# # Configuration

# CELL ********************

from pyspark.sql import functions as F
from pyspark.sql.types import *
from datetime import date, timedelta
import random

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Read environment specific variables

vars = notebookutils.variableLibrary.getLibrary('Supply Chain Variable Library')
ENVIRONMENT = vars.ENVIRONMENT
SEED = vars.SEED
PRODUCTS = vars.PRODUCTS
LOCATIONS = vars.LOCATIONS
DAYS = vars.DAYS
DEMAND_MULTIPLIER = vars.DEMAND_MULTIPLIER
STOCKOUT_PROBABILITY = vars.STOCKOUT_PROBABILITY

print("========================================")
print("Supply Chain Data Generation")
print("========================================")
print(f"Environment:          {ENVIRONMENT}")
print(f"Products:             {PRODUCTS}")
print(f"Locations:            {LOCATIONS}")
print(f"Days:                 {DAYS}")
print(f"Demand multiplier:    {DEMAND_MULTIPLIER}")
print(f"Stockout probability: {STOCKOUT_PROBABILITY}")
print("========================================")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # DimDate

# CELL ********************

start_date = date(2026, 1, 1)
dates = []

for i in range(DAYS):
    d = start_date + timedelta(days=i)

    dates.append((
        d,
        d.year,
        d.month,
        d.strftime("%B"),
        ((d.month - 1) // 3) + 1,
        d.isocalendar().week,
        d.strftime("%A")
    ))

date_schema = StructType([
    StructField("Date", DateType(), False),
    StructField("Year", IntegerType(), False),
    StructField("Month", IntegerType(), False),
    StructField("MonthName", StringType(), False),
    StructField("Quarter", IntegerType(), False),
    StructField("WeekOfYear", IntegerType(), False),
    StructField("DayOfWeek", StringType(), False)
])

df_date = spark.createDataFrame(dates, date_schema)

display(df_date)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # DimProduct

# CELL ********************

product_names = [
    "Laptop",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Headset",
    "Printer",
    "Tablet",
    "Smartphone",
    "Router",
    "Webcam",
    "USB Hub",
    "External SSD",
    "Docking Station",
    "Barcode Scanner",
    "Label Printer",
    "Office Chair",
    "Desk Lamp",
    "Power Adapter",
    "Network Switch",
    "Thermal Printer"
]

categories = [
    "Electronics",
    "Computer Accessories",
    "Office Equipment"
]

products = []

for i in range(PRODUCTS):
    name = product_names[i % len(product_names)]
    
    if name in ["Laptop", "Monitor", "Tablet", "Smartphone", "Router", "Network Switch"]:
        category = "Electronics"
    elif name in ["Printer", "Barcode Scanner", "Label Printer", "Thermal Printer"]:
        category = "Office Equipment"
    else:
        category = "Computer Accessories"

    unit_cost = round(random.uniform(20, 800), 2)

    products.append((
        i + 1,
        f"P{i + 1:03d}",
        name,
        category,
        unit_cost
    ))

product_schema = StructType([
    StructField("ProductKey", IntegerType(), False),
    StructField("ProductCode", StringType(), False),
    StructField("ProductName", StringType(), False),
    StructField("Category", StringType(), False),
    StructField("UnitCost", DoubleType(), False)
])

df_product = spark.createDataFrame(products, product_schema)

display(df_product)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # DimLocation

# CELL ********************

location_data = [
    ("Chicago Distribution Center", "Midwest", "Distribution Center"),
    ("Dallas Distribution Center", "South", "Distribution Center"),
    ("Atlanta Warehouse", "Southeast", "Warehouse"),
    ("Los Angeles Warehouse", "West", "Warehouse"),
    ("Newark Warehouse", "Northeast", "Warehouse"),
    ("Seattle Warehouse", "Northwest", "Warehouse")
]

locations = []

for i in range(LOCATIONS):
    name, region, location_type = location_data[i]

    locations.append((
        i + 1,
        f"L{i + 1:03d}",
        name,
        region,
        location_type
    ))

location_schema = StructType([
    StructField("LocationKey", IntegerType(), False),
    StructField("LocationCode", StringType(), False),
    StructField("LocationName", StringType(), False),
    StructField("Region", StringType(), False),
    StructField("LocationType", StringType(), False)
])

df_location = spark.createDataFrame(locations, location_schema)

display(df_location)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Fact Inventory

# CELL ********************

suppliers_df = spark.sql("SELECT * FROM OmniRoute_Lakehouse.dbo.DimSupplier LIMIT 1000")
suppliers = suppliers_df.collect()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

fact_rows = []

# Assign one supplier to each Product + Location combination.
# This keeps the supplier consistent across all dates.
product_location_suppliers = {}

for product in products:
    product_key = product[0]

    for location in locations:
        location_key = location[0]

        # Randomly assign one supplier to this Product + Location combination
        supplier = random.choice(suppliers)
        supplier_key = supplier[0]

        product_location_suppliers[(product_key, location_key)] = supplier_key


for d in dates:
    inventory_date = d[0]

    for product in products:
        product_key = product[0]
        unit_cost = product[4]

        for location in locations:
            location_key = location[0]

            # Get the supplier assigned to this Product + Location
            supplier_key = product_location_suppliers[
                (product_key, location_key)
            ]

            # Base inventory level
            base_inventory = random.randint(50, 250)

            # Demand varies by environment
            demand = max(
                1,
                int(
                    random.randint(5, 40)
                    * DEMAND_MULTIPLIER
                )
            )

            # Simple safety-stock calculation
            safety_stock = int(
                demand * random.uniform(1.5, 2.5)
            )

            reorder_point = safety_stock + demand * 2

            # Some inventory gets replenished
            received = 0

            if random.random() < 0.25:
                received = random.randint(20, 100)

            quantity_on_hand = max(
                0,
                base_inventory + received - demand
            )

            # Add a small environment-specific chance of stockout
            if random.random() < STOCKOUT_PROBABILITY:
                quantity_on_hand = random.randint(
                    0,
                    max(1, demand // 2)
                )

            stockout_flag = 1 if quantity_on_hand == 0 else 0

            fact_rows.append((
                inventory_date,
                product_key,
                location_key,
                supplier_key,
                quantity_on_hand,
                safety_stock,
                reorder_point,
                received,
                demand,
                stockout_flag,
                unit_cost
            ))


fact_schema = StructType([
    StructField("Date", DateType(), False),
    StructField("ProductKey", IntegerType(), False),
    StructField("LocationKey", IntegerType(), False),
    StructField("SupplierKey", IntegerType(), False),
    StructField("QuantityOnHand", IntegerType(), False),
    StructField("SafetyStock", IntegerType(), False),
    StructField("ReorderPoint", IntegerType(), False),
    StructField("UnitsReceived", IntegerType(), False),
    StructField("UnitsConsumed", IntegerType(), False),
    StructField("StockoutFlag", IntegerType(), False),
    StructField("UnitCost", DoubleType(), False)
])


df_inventory = spark.createDataFrame(
    fact_rows,
    fact_schema
)


# Add inventory value
df_inventory = df_inventory.withColumn(
    "InventoryValue",
    F.round(
        F.col("QuantityOnHand") * F.col("UnitCost"),
        2
    )
)


display(df_inventory.limit(100))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Write to Lakehouse  
# This assumes an attached, default Lakehouse.

# CELL ********************

print("Writing tables to Lakehouse...")

df_date.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("DimDate")

df_product.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("DimProduct")

df_location.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("DimLocation")

df_inventory.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("FactInventory")

print("Tables written successfully.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Validation

# CELL ********************

print()
print("========================================")
print("Generation completed successfully")
print("========================================")

print(f"Environment:   {ENVIRONMENT}")
print()

print(f"DimDate:       {df_date.count():,} rows")
print(f"DimProduct:    {df_product.count():,} rows")
print(f"DimLocation:   {df_location.count():,} rows")
print(f"FactInventory: {df_inventory.count():,} rows")

print()
print("Inventory summary:")

summary = df_inventory.agg(
    F.round(F.avg("QuantityOnHand"), 2).alias("AvgInventory"),
    F.round(F.avg("UnitsConsumed"), 2).alias("AvgDailyConsumption"),
    F.round(F.sum("InventoryValue"), 2).alias("TotalInventoryValue"),
    F.round(F.avg("StockoutFlag") * 100, 2).alias("StockoutRatePct")
)

display(summary)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
