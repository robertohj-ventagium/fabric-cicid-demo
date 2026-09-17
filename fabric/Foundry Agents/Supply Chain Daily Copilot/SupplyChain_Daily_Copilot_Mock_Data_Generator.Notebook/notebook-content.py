# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0a819558-ac91-4db5-978e-aad1fe83ce96",
# META       "default_lakehouse_name": "Supply_Chain_Lakehouse",
# META       "default_lakehouse_workspace_id": "1beb3139-2c5d-4cb3-b416-c46404555b49",
# META       "known_lakehouses": [
# META         {
# META           "id": "0a819558-ac91-4db5-978e-aad1fe83ce96"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Mock Supply Chain Lakehouse Generator
# This notebook generates deterministic mock data for a Supply Chain Daily Copilot demo.
# 
# > **Note:** This is a starter scaffold with reusable generation functions.

# MARKDOWN ********************

# # Configuration

# CELL ********************

import pandas as pd
import numpy as np
from datetime import datetime
rng=np.random.default_rng(42)


# Some of these values used for reference only, in the corresponding sections
warehouses=['WH_DAL','WH_CHI','WH_ATL','WH_PHX','WH_NYC','WH_LAX']
customers=[f'Customer_{i:02d}' for i in range(1,41)]
suppliers=['Pacific Packaging','Global Plastics','Fresh Farms','Andes Ingredients','Atlantic Chemicals','Nippon Components','Nordic Paper','Shenzhen Manufacturing','Brasil Oils','Alpine Dairy','Prime Resins','Ocean Foods','Maple Paper','Evergreen Ag','Sunrise Ingredients']
products=[f'Product_{i:03d}' for i in range(1,81)]
ports=['Los Angeles','Long Beach','Houston','New York','Seattle','Vancouver']


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# for the demo, just keep 10 ~ days
dates = pd.date_range("2026-07-06", "2026-07-17")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Data Sources

# MARKDOWN ********************

# ## Calendar

# CELL ********************

# Generate calendar

meeting_types = [
    "Daily Operations Review",
    "Supplier Review",
    "Customer Escalation",
    "Inventory Review",
    "Forecast Review",
    "Transportation Review",
    "Executive Supply Chain Brief",
    "Production Planning"
]

owners = [
    "Emily Rodriguez",
    "Michael Chen",
    "Sarah Johnson",
    "David Patel",
    "Laura Gomez"
]

preparation_actions = {
    "Daily Operations Review": [
        "Review KPI exceptions and operational alerts",
        "Check inventory shortages and order risks"
    ],
    "Supplier Review": [
        "Review supplier delays and open recovery actions",
        "Analyze supplier performance trends"
    ],
    "Customer Escalation": [
        "Review delayed orders and customer impact",
        "Prepare recovery plan"
    ],
    "Inventory Review": [
        "Analyze low inventory locations and coverage",
        "Review replenishment priorities"
    ],
    "Forecast Review": [
        "Review forecast accuracy and demand changes",
        "Analyze upcoming demand risks"
    ],
    "Transportation Review": [
        "Review delayed containers and logistics risks",
        "Check port disruptions"
    ],
    "Executive Supply Chain Brief": [
        "Prepare summary of top supply chain risks",
        "Highlight mitigation actions"
    ],
    "Production Planning": [
        "Review material availability and production constraints",
        "Validate production priorities"
    ]
}

rows = []

meeting_id = 1

for d in dates:

    # Between 2 and 6 meetings per day
    n_meetings = rng.integers(2, 7)

    for _ in range(n_meetings):

        meeting_type = rng.choice(
            meeting_types,
            p=[0.25, 0.15, 0.08, 0.15, 0.12, 0.10, 0.05, 0.10]
        )

        start_hour = int(rng.integers(8, 16))
        start_min = int(rng.choice([0, 30]))

        duration = int(rng.choice([30, 60]))

        supplier = None
        customer = None

        if meeting_type == "Supplier Review":
            supplier = rng.choice(suppliers)

        if meeting_type == "Customer Escalation":
            customer = rng.choice(customers)

        warehouse = rng.choice(warehouses)

        priority = rng.choice(
            ["Low", "Medium", "High"],
            p=[0.35, 0.50, 0.15]
        )

        risk_map = {
            "Daily Operations Review": "Operational exceptions",
            "Supplier Review": "Supplier performance risk",
            "Customer Escalation": "Customer service risk",
            "Inventory Review": "Inventory availability risk",
            "Forecast Review": "Demand uncertainty",
            "Transportation Review": "Logistics disruption risk",
            "Executive Supply Chain Brief": "Business continuity risk",
            "Production Planning": "Production capacity risk"
        }

        end_hour = start_hour + duration // 60
        end_min = start_min + duration % 60

        if end_min >= 60:
            end_hour += 1
            end_min -= 60

        rows.append({
            "meeting_id": f"MTG{meeting_id:05d}",
            "meeting_date": d.date(),
            "meeting_start": f"{start_hour:02d}:{start_min:02d}",
            "meeting_end": f"{end_hour:02d}:{end_min:02d}",
            "owner": rng.choice(owners),
            "meeting_type": meeting_type,
            "supplier_name": supplier,
            "customer_name": customer,
            "warehouse": warehouse,
            "priority": priority,
            "title": meeting_type,
            "description": f"{meeting_type} for {warehouse}",
            "preparation_needed": rng.choice(preparation_actions[meeting_type]),
            "related_risk": risk_map[meeting_type],
            "status": rng.choice(
                ["Scheduled", "Completed"],
                p=[0.7, 0.3]
            )
        })

        meeting_id += 1


df = pd.DataFrame(rows)

print(df.head())
print(f"\nTotal meetings: {len(df):,}")

# Save as table
spark.createDataFrame(df).write.mode("overwrite").format("delta").saveAsTable("calendar")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Emails

# CELL ********************

# -------------------------------------------------------
# Emails
# July 6 - July 17, 2026
# -------------------------------------------------------

import pandas as pd

emails = pd.DataFrame([

# =====================================================================
# JULY 6
# =====================================================================

{
"email_id":"EMAIL000001",
"datetime":"2026-07-06 08:12",
"sender":"planner@northwind.com",
"recipient":"emily.rodriguez@northwind.com",
"subject":"Weekly Supply Chain Planning",
"body":"Please review inventory and customer demand before tomorrow's planning meeting.",
"category":"Operations",
"priority":"Medium",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_DAL",
"product":None,
"order_id":None,
"requires_action":True
},

{
"email_id":"EMAIL000002",
"datetime":"2026-07-06 09:45",
"sender":"supplier@pacificpackaging.com",
"recipient":"buyer@northwind.com",
"subject":"Shipment departed on schedule",
"body":"Packaging materials departed Los Angeles this morning. ETA remains July 10.",
"category":"Supplier",
"priority":"Low",
"customer_name":None,
"supplier_name":"Pacific Packaging",
"warehouse":"WH_DAL",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":False
},

{
"email_id":"EMAIL000003",
"datetime":"2026-07-06 15:20",
"sender":"sales@northwind.com",
"recipient":"planner@northwind.com",
"subject":"CostMart promotion confirmed",
"body":"CostMart confirmed the July beverage promotion. Forecast should increase approximately 15%.",
"category":"Forecast",
"priority":"Medium",
"customer_name":"CostMart",
"supplier_name":None,
"warehouse":"WH_DAL",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":True
},

# =====================================================================
# JULY 7
# =====================================================================

{
"email_id":"EMAIL000004",
"datetime":"2026-07-07 09:10",
"sender":"warehouse@northwind.com",
"recipient":"planner@northwind.com",
"subject":"Safety stock warning",
"body":"Spark Cola 355ml inventory is approaching safety stock in WH_PHX.",
"category":"Inventory",
"priority":"High",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_PHX",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":True
},

{
"email_id":"EMAIL000005",
"datetime":"2026-07-07 11:35",
"sender":"transport@northwind.com",
"recipient":"logistics@northwind.com",
"subject":"Container loaded",
"body":"Container CONT-10452 has departed Los Angeles.",
"category":"Transportation",
"priority":"Low",
"supplier_name":"Pacific Packaging",
"customer_name":None,
"warehouse":"WH_DAL",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":False
},

# =====================================================================
# JULY 8
# =====================================================================

{
"email_id":"EMAIL000006",
"datetime":"2026-07-08 08:40",
"sender":"forecast@northwind.com",
"recipient":"planner@northwind.com",
"subject":"Demand forecast updated",
"body":"Southwest beverage demand increased due to expected heat wave.",
"category":"Forecast",
"priority":"Medium",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_PHX",
"product":"Spark Cola 2L",
"order_id":None,
"requires_action":True
},

{
"email_id":"EMAIL000007",
"datetime":"2026-07-08 14:18",
"sender":"buyer@northwind.com",
"recipient":"supplier@pacificpackaging.com",
"subject":"Can additional packaging be expedited?",
"body":"Forecast has increased substantially. Can you ship additional packaging this week?",
"category":"Supplier",
"priority":"Medium",
"customer_name":None,
"supplier_name":"Pacific Packaging",
"warehouse":"WH_DAL",
"product":"Spark Cola 2L",
"order_id":None,
"requires_action":True
},

# =====================================================================
# JULY 9
# =====================================================================

{
"email_id":"EMAIL000008",
"datetime":"2026-07-09 10:05",
"sender":"supplier@pacificpackaging.com",
"recipient":"buyer@northwind.com",
"subject":"Additional capacity confirmed",
"body":"We can support an extra shipment next week.",
"category":"Supplier",
"priority":"Low",
"customer_name":None,
"supplier_name":"Pacific Packaging",
"warehouse":"WH_DAL",
"product":"Spark Cola 2L",
"order_id":None,
"requires_action":False
},

{
"email_id":"EMAIL000009",
"datetime":"2026-07-09 16:22",
"sender":"warehouse@northwind.com",
"recipient":"operations@northwind.com",
"subject":"Inventory transfer recommended",
"body":"Recommend transferring inventory from WH_DAL to WH_PHX.",
"category":"Inventory",
"priority":"Medium",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_PHX",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":True
},

# =====================================================================
# JULY 10
# =====================================================================

{
"email_id":"EMAIL000010",
"datetime":"2026-07-10 09:00",
"sender":"customer@costmart.com",
"recipient":"sales@northwind.com",
"subject":"Promotion launch confirmed",
"body":"Stores are fully stocked for Monday's promotion.",
"category":"Customer",
"priority":"Low",
"customer_name":"CostMart",
"supplier_name":None,
"warehouse":"WH_DAL",
"product":"Spark Cola 355ml",
"order_id":"ORD000123",
"requires_action":False
},

{
"email_id":"EMAIL000011",
"datetime":"2026-07-10 15:12",
"sender":"planner@northwind.com",
"recipient":"operations@northwind.com",
"subject":"Inventory transfer approved",
"body":"Move 1,500 cases from WH_DAL to WH_PHX.",
"category":"Operations",
"priority":"High",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_DAL",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":True
},

# =====================================================================
# JULY 11
# =====================================================================

{
"email_id":"EMAIL000012",
"datetime":"2026-07-11 10:02",
"sender":"transport@northwind.com",
"recipient":"warehouse@northwind.com",
"subject":"Transfer shipment dispatched",
"body":"Truck departed Dallas this morning.",
"category":"Transportation",
"priority":"Low",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_DAL",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":False
},

# =====================================================================
# JULY 12
# =====================================================================

{
"email_id":"EMAIL000013",
"datetime":"2026-07-12 13:11",
"sender":"warehouse@northwind.com",
"recipient":"planner@northwind.com",
"subject":"Transfer received",
"body":"Inventory successfully received at WH_PHX.",
"category":"Inventory",
"priority":"Low",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_PHX",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":False
},

# =====================================================================
# JULY 14
# =====================================================================

{
"email_id":"EMAIL000014",
"datetime":"2026-07-14 09:25",
"sender":"sales@northwind.com",
"recipient":"operations@northwind.com",
"subject":"Promotion exceeded expectations",
"body":"Sales exceeded forecast by approximately 18%.",
"category":"Forecast",
"priority":"Medium",
"customer_name":"CostMart",
"supplier_name":None,
"warehouse":"WH_PHX",
"product":"Spark Cola 355ml",
"order_id":None,
"requires_action":True
},

# =====================================================================
# JULY 16
# =====================================================================

{
"email_id":"EMAIL000015",
"datetime":"2026-07-16 08:44",
"sender":"planner@northwind.com",
"recipient":"leadership@northwind.com",
"subject":"Heat wave impact summary",
"body":"Inventory actions successfully prevented stockouts despite increased demand.",
"category":"Operations",
"priority":"Medium",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_PHX",
"product":None,
"order_id":None,
"requires_action":False
},

# =====================================================================
# JULY 17
# =====================================================================

{
"email_id":"EMAIL000016",
"datetime":"2026-07-17 11:30",
"sender":"emily.rodriguez@northwind.com",
"recipient":"supplychain@northwind.com",
"subject":"Weekly supply chain recap",
"body":"Excellent execution this week. Inventory transfers and supplier collaboration avoided customer service issues during the demand spike.",
"category":"Operations",
"priority":"Low",
"customer_name":None,
"supplier_name":None,
"warehouse":"WH_PHX",
"product":None,
"order_id":None,
"requires_action":False
}

])

emails["datetime"] = pd.to_datetime(emails["datetime"])

print(emails.head())
print(f"\nTotal meetings: {len(emails):,}")

# Save as table
spark.createDataFrame(emails).write.mode("overwrite").format("delta").saveAsTable("emails")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## KPIs

# CELL ********************

# -------------------------------------------------------
# KPIs Daily
# July 6 - July 17, 2026
# -------------------------------------------------------

import pandas as pd

dates = pd.date_range("2026-07-06", "2026-07-17")

warehouses = [
    "WH_DAL",
    "WH_CHI",
    "WH_ATL",
    "WH_PHX",
    "WH_NYC",
    "WH_LAX"
]

rows = []

for d in dates:

    for wh in warehouses:

        # ----------------------------
        # Normal business
        # ----------------------------

        otif = 98.5
        fill_rate = 99.2
        forecast_accuracy = 95.0
        inventory_turns = 8.4
        inventory_value = 4_500_000
        backorders = 2
        late_orders = 1
        stockouts = 0

        # ------------------------------------------------
        # Heat wave affects Phoenix between Jul 8-12
        # ------------------------------------------------

        if wh == "WH_PHX":

            if d == pd.Timestamp("2026-07-08"):
                forecast_accuracy = 91.0

            elif d == pd.Timestamp("2026-07-09"):
                forecast_accuracy = 89.0
                fill_rate = 97.8
                backorders = 8

            elif d == pd.Timestamp("2026-07-10"):
                otif = 96.2
                fill_rate = 96.8
                forecast_accuracy = 88.5
                backorders = 15
                late_orders = 9

            elif d == pd.Timestamp("2026-07-11"):
                otif = 95.8
                fill_rate = 96.3
                backorders = 17
                late_orders = 10

            elif d == pd.Timestamp("2026-07-12"):
                otif = 96.8
                fill_rate = 97.4
                backorders = 8
                late_orders = 5

            elif d >= pd.Timestamp("2026-07-13"):
                otif = 98.4
                fill_rate = 99.1
                forecast_accuracy = 96.2
                backorders = 1
                late_orders = 1

        # ------------------------------------------------
        # Dallas ships inventory to Phoenix
        # ------------------------------------------------

        if wh == "WH_DAL":

            if d == pd.Timestamp("2026-07-10"):
                inventory_value = 4_350_000

            elif d == pd.Timestamp("2026-07-11"):
                inventory_value = 4_250_000
                inventory_turns = 8.8

            elif d == pd.Timestamp("2026-07-12"):
                inventory_value = 4_280_000

        rows.append({

            "date": d.date(),

            "warehouse": wh,

            "otif": round(otif,1),

            "fill_rate": round(fill_rate,1),

            "forecast_accuracy": round(forecast_accuracy,1),

            "inventory_turns": round(inventory_turns,1),

            "inventory_value": inventory_value,

            "backorders": backorders,

            "late_orders": late_orders,

            "stockouts": stockouts

        })

kpis_daily = pd.DataFrame(rows)

display(kpis_daily)

# Fabric
spark.createDataFrame(kpis_daily)\
    .write.mode("overwrite")\
    .format("delta")\
    .saveAsTable("kpis_daily")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Orders

# CELL ********************

# -------------------------------------------------------
# Orders
# July 6 - July 17, 2026
# -------------------------------------------------------

import pandas as pd
import numpy as np

rng = np.random.default_rng(42)

dates = pd.date_range("2026-07-06", "2026-07-17")

customers = [
    "CostMart",
    "MegaRetail",
    "Fresh Market",
    "Value Stores",
    "QuickShop",
    "SuperFoods"
]

warehouses = [
    "WH_DAL",
    "WH_CHI",
    "WH_ATL",
    "WH_PHX",
    "WH_NYC",
    "WH_LAX"
]

products = [
    "Spark Cola 355ml",
    "Spark Cola 2L",
    "Fresh Juice Orange",
    "Fresh Juice Apple",
    "Protein Bar Chocolate",
    "Protein Bar Peanut",
    "Cleaning Spray",
    "Paper Towels 12pk"
]

rows = []

order_number = 100000

for d in dates:

    # -------------------------
    # Daily order volume
    # -------------------------

    n_orders = 18

    if d >= pd.Timestamp("2026-07-08"):
        n_orders = 24

    if d >= pd.Timestamp("2026-07-10"):
        n_orders = 28

    if d >= pd.Timestamp("2026-07-13"):
        n_orders = 22

    for _ in range(n_orders):
        customer = rng.choice(customers)
        warehouse = rng.choice(warehouses)
        product = rng.choice(products)
        qty = int(rng.integers(100,800))
        requested_date = d + pd.Timedelta(days=2)
        promised_date = requested_date
        actual_ship_date = requested_date
        status = "Shipped"
        delay_reason = None
        priority = "Normal"

        # ----------------------------------------------------
        # CostMart beverage promotion
        # ----------------------------------------------------

        if d >= pd.Timestamp("2026-07-08"):
            if rng.random() < 0.45:
                customer = "CostMart"
                warehouse = "WH_PHX"
                product = rng.choice([
                    "Spark Cola 355ml",
                    "Spark Cola 2L"
                ])

                qty = int(rng.integers(900,1800))

        # ----------------------------------------------------
        # Inventory shortage
        # ----------------------------------------------------

        if warehouse == "WH_PHX":
            if product in [
                "Spark Cola 355ml",
                "Spark Cola 2L"
            ]:

                if d in [
                    pd.Timestamp("2026-07-09"),
                    pd.Timestamp("2026-07-10"),
                    pd.Timestamp("2026-07-11")
                ]:

                    if rng.random() < 0.60:
                        actual_ship_date = requested_date + pd.Timedelta(days=2)
                        status = "Delayed"
                        delay_reason = "Inventory Shortage"
                        priority = "High"

        rows.append({
            "order_id": f"ORD{order_number}",
            "order_date": d.date(),
            "customer_name": customer,
            "warehouse": warehouse,
            "product": product,
            "order_qty": qty,
            "requested_ship_date": requested_date.date(),
            "promised_ship_date": promised_date.date(),
            "actual_ship_date": actual_ship_date.date(),
            "order_status": status,
            "delay_reason": delay_reason,
            "priority": priority
        })

        order_number += 1

orders = pd.DataFrame(rows)
display(orders)

# Fabric
spark.createDataFrame(orders)\
    .write.mode("overwrite")\
    .format("delta")\
    .saveAsTable("orders")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Inventory

# CELL ********************

# -------------------------------------------------------
# Inventory Daily
# July 6 - July 17, 2026
# -------------------------------------------------------

import pandas as pd

dates = pd.date_range("2026-07-06", "2026-07-17")

warehouses = [
    "WH_DAL",
    "WH_CHI",
    "WH_ATL",
    "WH_PHX",
    "WH_NYC",
    "WH_LAX"
]

products = [
    "Spark Cola 355ml",
    "Spark Cola 2L",
    "Fresh Juice Orange",
    "Fresh Juice Apple",
    "Protein Bar Chocolate",
    "Protein Bar Peanut",
    "Cleaning Spray",
    "Paper Towels 12pk"
]

rows = []

for d in dates:

    for wh in warehouses:

        for product in products:

            # --------------------------------------------------
            # Default inventory
            # --------------------------------------------------

            on_hand = 2500
            safety_stock = 1000
            reserved = 300
            inbound = 600
            available = on_hand - reserved
            inventory_status = "Healthy"

            # ==================================================
            # PHOENIX HEAT WAVE STORY
            # ==================================================

            if wh == "WH_PHX" and product in [
                "Spark Cola 355ml",
                "Spark Cola 2L"
            ]:

                if d == pd.Timestamp("2026-07-06"):
                    on_hand = 1700

                elif d == pd.Timestamp("2026-07-07"):
                    on_hand = 1300

                elif d == pd.Timestamp("2026-07-08"):
                    on_hand = 1050

                elif d == pd.Timestamp("2026-07-09"):
                    on_hand = 850
                    inventory_status = "Below Safety Stock"

                elif d == pd.Timestamp("2026-07-10"):
                    on_hand = 620
                    inventory_status = "Critical"

                elif d == pd.Timestamp("2026-07-11"):
                    on_hand = 480
                    inventory_status = "Critical"

                elif d == pd.Timestamp("2026-07-12"):
                    # Inventory transfer received
                    on_hand = 1750
                    inbound = 0
                    inventory_status = "Recovered"

                elif d >= pd.Timestamp("2026-07-13"):
                    on_hand = 1650
                    inventory_status = "Healthy"

            # ==================================================
            # DALLAS SHIPS INVENTORY
            # ==================================================

            if wh == "WH_DAL" and product in [
                "Spark Cola 355ml",
                "Spark Cola 2L"
            ]:

                if d <= pd.Timestamp("2026-07-09"):
                    on_hand = 3200

                elif d == pd.Timestamp("2026-07-10"):
                    on_hand = 2500

                elif d == pd.Timestamp("2026-07-11"):
                    on_hand = 1800

                elif d == pd.Timestamp("2026-07-12"):
                    on_hand = 1700

                else:
                    on_hand = 1900

            available = on_hand - reserved

            days_of_supply = round(on_hand / 220, 1)

            rows.append({

                "date": d.date(),
                "warehouse": wh,
                "product": product,
                "on_hand_qty": on_hand,
                "reserved_qty": reserved,
                "available_qty": available,
                "inbound_qty": inbound,
                "safety_stock_qty": safety_stock,
                "days_of_supply": days_of_supply,
                "inventory_status": inventory_status
            })

inventory_daily = pd.DataFrame(rows)

display(inventory_daily)

# Fabric
spark.createDataFrame(inventory_daily)\
    .write.mode("overwrite")\
    .format("delta")\
    .saveAsTable("inventory_daily")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Supplier Updates

# CELL ********************

# Generate supplier_updates

rows = []

suppliers_updates = [
    {
        "supplier_id": "SUP001",
        "supplier_name": "Pacific Packaging",
        "update_type": "Production Delay",
        "severity": "High",
        "status": "Monitoring",
        "message": "Production line maintenance took longer than expected, delaying packaging material availability.",
        "affected_product": "Product_012",
        "affected_region": "North America",
        "affected_warehouse": "WH_PHX",   # Packaging shortage contributes to Phoenix issues
        "expected_impact": "Potential delay in customer shipments due to reduced packaging availability.",
        "action_required": "Monitor inventory coverage and prioritize critical orders."
    },
    {
        "supplier_id": "SUP002",
        "supplier_name": "Global Plastics",
        "update_type": "Capacity Constraint",
        "severity": "Medium",
        "status": "Open",
        "message": "Supplier is operating at reduced capacity due to unexpected demand increase.",
        "affected_product": "Product_025",
        "affected_region": "United States",
        "affected_warehouse": "WH_DAL",
        "expected_impact": "Lead times may increase by 5-7 days.",
        "action_required": "Review purchase order priorities and alternative supply options."
    },
    {
        "supplier_id": "SUP003",
        "supplier_name": "Fresh Farms",
        "update_type": "Quality Issue",
        "severity": "Critical",
        "status": "Open",
        "message": "Quality inspection detected non-conforming material in the latest production batch.",
        "affected_product": "Product_041",
        "affected_region": "Mexico",
        "affected_warehouse": "WH_PHX",   # Product_041 is also on delayed container CONT005
        "expected_impact": "Potential supply interruption if replacement shipment is delayed.",
        "action_required": "Expedite replacement material and validate quality results."
    },
    {
        "supplier_id": "SUP004",
        "supplier_name": "Andes Ingredients",
        "update_type": "Shipment Update",
        "severity": "Low",
        "status": "Resolved",
        "message": "Supplier confirmed shipment departed earlier than planned.",
        "affected_product": "Product_008",
        "affected_region": "South America",
        "affected_warehouse": "WH_PHX",   # Same supplier as CONT005
        "expected_impact": "Inventory position expected to improve.",
        "action_required": "Continue standard monitoring."
    },
    {
        "supplier_id": "SUP005",
        "supplier_name": "Nippon Components",
        "update_type": "Logistics Delay",
        "severity": "High",
        "status": "Monitoring",
        "message": "Shipment departure delayed due to port congestion affecting export schedules.",
        "affected_product": "Product_063",
        "affected_region": "Asia",
        "affected_warehouse": "WH_LAX",
        "expected_impact": "Estimated arrival delay of 7 days.",
        "action_required": "Evaluate alternate transportation options."
    },
    {
        "supplier_id": "SUP006",
        "supplier_name": "Nordic Paper",
        "update_type": "Capacity Increase",
        "severity": "Low",
        "status": "Resolved",
        "message": "Supplier increased weekly production capacity after equipment upgrade.",
        "affected_product": "Product_014",
        "affected_region": "Europe",
        "affected_warehouse": "WH_CHI",
        "expected_impact": "Improved supply availability.",
        "action_required": "Consider increasing future allocation."
    },
    {
        "supplier_id": "SUP007",
        "supplier_name": "Shenzhen Manufacturing",
        "update_type": "Production Delay",
        "severity": "High",
        "status": "Open",
        "message": "Component production delayed due to shortage of electronic parts.",
        "affected_product": "Product_052",
        "affected_region": "Asia",
        "affected_warehouse": "WH_PHX",   # Same supplier as CONT001
        "expected_impact": "Risk of missing planned production schedule.",
        "action_required": "Review alternate suppliers and inventory buffers."
    },
    {
        "supplier_id": "SUP008",
        "supplier_name": "Brasil Oils",
        "update_type": "Material Availability",
        "severity": "Medium",
        "status": "Monitoring",
        "message": "Supplier reported limited availability of raw materials due to seasonal demand.",
        "affected_product": "Product_033",
        "affected_region": "South America",
        "affected_warehouse": "WH_NYC",
        "expected_impact": "Possible allocation restrictions.",
        "action_required": "Validate demand priorities."
    },
    {
        "supplier_id": "SUP009",
        "supplier_name": "Alpine Dairy",
        "update_type": "Shipment Confirmation",
        "severity": "Low",
        "status": "Resolved",
        "message": "Supplier confirmed shipment delivered according to schedule.",
        "affected_product": "Product_019",
        "affected_region": "North America",
        "affected_warehouse": "WH_ATL",
        "expected_impact": "No supply impact expected.",
        "action_required": "No action required."
    },
    {
        "supplier_id": "SUP010",
        "supplier_name": "Prime Resins",
        "update_type": "Raw Material Shortage",
        "severity": "Critical",
        "status": "Open",
        "message": "Supplier experiencing shortage of key resin inputs affecting production plans.",
        "affected_product": "Product_070",
        "affected_region": "United States",
        "affected_warehouse": "WH_DAL",
        "expected_impact": "High risk of production disruption.",
        "action_required": "Escalate supplier recovery plan."
    },
    {
        "supplier_id": "SUP011",
        "supplier_name": "Ocean Foods",
        "update_type": "Weather Impact",
        "severity": "Medium",
        "status": "Monitoring",
        "message": "Severe weather conditions affected supplier transportation routes.",
        "affected_product": "Product_045",
        "affected_region": "Gulf Coast",
        "affected_warehouse": "WH_LAX",
        "expected_impact": "Potential delivery delay of 3-4 days.",
        "action_required": "Monitor logistics updates."
    }
]


for i, d in enumerate(pd.date_range("2026-07-07", "2026-07-17")):
    update = suppliers_updates[i % len(suppliers_updates)].copy()
    update["date"] = d.date()
    rows.append(update)

df = pd.DataFrame(rows)

print(df.head())

# Fabric example:
spark.createDataFrame(df).write.mode('overwrite').format('delta').saveAsTable('supplier_updates')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Weather

# CELL ********************

# Generate weather
rows=[]
# TODO: extend logic as desired
for d in dates[:10]:
    rows.append({'date':d})
df=pd.DataFrame(rows)
print(df.head())
# Fabric example:
# spark.createDataFrame(df).write.mode('overwrite').format('delta').saveAsTable('weather')


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Container Status

# CELL ********************

# Generate container_status

rows = []

container_events = [
    {
        "container_id": "CONT001",
        "supplier_name": "Shenzhen Manufacturing",
        "origin_port": "Shenzhen",
        "destination_port": "Phoenix",
        "destination_warehouse": "WH_PHX",
        "status": "Delayed",
        "estimated_arrival_date": "2026-07-14",
        "days_delayed": 5,
        "delay_reason": "Rail transportation delay after port discharge",
        "risk_level": "High",
        "affected_products": "Product_052, Product_063",
        "recommended_action": "Review inventory coverage and consider expedited transportation"
    },
    {
        "container_id": "CONT002",
        "supplier_name": "Nippon Components",
        "origin_port": "Tokyo",
        "destination_port": "Long Beach",
        "destination_warehouse": "WH_LAX",# Long Beach -> LAX DC
        "status": "In Transit",
        "estimated_arrival_date": "2026-07-12",
        "days_delayed": 0,
        "delay_reason": "None",
        "risk_level": "Low",
        "affected_products": "Product_021",
        "recommended_action": "Continue monitoring vessel progress"
    },
    {
        "container_id": "CONT003",
        "supplier_name": "Pacific Packaging",
        "origin_port": "Vancouver",
        "destination_port": "Seattle",
        "destination_warehouse": "WH_LAX",# Seattle import redistributed
        "status": "Customs Hold",
        "estimated_arrival_date": "2026-07-18",
        "days_delayed": 3,
        "delay_reason": "Documentation validation issue",
        "risk_level": "Medium",
        "affected_products": "Product_012",
        "recommended_action": "Coordinate with customs broker to accelerate clearance"
    },
    {
        "container_id": "CONT004",
        "supplier_name": "Global Plastics",
        "origin_port": "Houston",
        "destination_port": "Houston",
        "destination_warehouse": "WH_DAL",# Houston -> Dallas DC
        "status": "Arrived",
        "estimated_arrival_date": "2026-07-09",
        "days_delayed": 0,
        "delay_reason": "None",
        "risk_level": "Low",
        "affected_products": "Product_025",
        "recommended_action": "Schedule warehouse receiving"
    },
    {
        "container_id": "CONT005",
        "supplier_name": "Andes Ingredients",
        "origin_port": "Vancouver",
        "destination_port": "Phoenix",
        "destination_warehouse": "WH_PHX",
        "status": "Delayed",
        "estimated_arrival_date": "2026-07-16",
        "days_delayed": 4,
        "delay_reason": "Severe weather impacting rail transportation to Phoenix",
        "risk_level": "High",
        "affected_products": "Product_008, Product_041",
        "recommended_action": "Evaluate alternate inventory allocation and consider inventory transfer from WH_DAL"
    },
    {
        "container_id": "CONT006",
        "supplier_name": "Brasil Oils",
        "origin_port": "Houston",
        "destination_port": "New York",
        "destination_warehouse": "WH_NYC",# New York
        "status": "In Transit",
        "estimated_arrival_date": "2026-07-15",
        "days_delayed": 1,
        "delay_reason": "Minor transportation disruption",
        "risk_level": "Medium",
        "affected_products": "Product_033",
        "recommended_action": "Monitor delivery schedule"
    },
    {
        "container_id": "CONT007",
        "supplier_name": "Nordic Paper",
        "origin_port": "Seattle",
        "destination_port": "Los Angeles",
        "destination_warehouse": "WH_LAX",# Los Angeles
        "status": "Delivered",
        "estimated_arrival_date": "2026-07-07",
        "days_delayed": 0,
        "delay_reason": "None",
        "risk_level": "Low",
        "affected_products": "Product_014",
        "recommended_action": "No action required"
    },
    {
        "container_id": "CONT008",
        "supplier_name": "Prime Resins",
        "origin_port": "Houston",
        "destination_port": "New York",
        "destination_warehouse": "WH_NYC",# New York
        "status": "Loading",
        "estimated_arrival_date": "2026-07-20",
        "days_delayed": 0,
        "delay_reason": "None",
        "risk_level": "Low",
        "affected_products": "Product_070",
        "recommended_action": "Monitor departure confirmation"
    },
    {
        "container_id": "CONT009",
        "supplier_name": "Ocean Foods",
        "origin_port": "Long Beach",
        "destination_port": "Los Angeles",
        "destination_warehouse": "WH_LAX",# Los Angeles
        "status": "Delayed",
        "estimated_arrival_date": "2026-07-19",
        "days_delayed": 6,
        "delay_reason": "Weather disruption and terminal backlog",
        "risk_level": "Critical",
        "affected_products": "Product_045",
        "recommended_action": "Escalate logistics recovery plan"
    },
    {
        "container_id": "CONT010",
        "supplier_name": "Alpine Dairy",
        "origin_port": "Vancouver",
        "destination_port": "Seattle",
        "destination_warehouse": "WH_PHX",# Seattle -> Phoenix DC
        "status": "Delivered",
        "estimated_arrival_date": "2026-07-10",
        "days_delayed": 0,
        "delay_reason": "None",
        "risk_level": "Low",
        "affected_products": "Product_019",
        "recommended_action": "Complete receiving process"
    },
    {
        "container_id": "CONT011",
        "supplier_name": "Evergreen Ag",
        "origin_port": "Los Angeles",
        "destination_port": "Houston",
        "destination_warehouse": "WH_DAL",# Houston -> Dallas
        "status": "In Transit",
        "estimated_arrival_date": "2026-07-17",
        "days_delayed": 2,
        "delay_reason": "Rail transportation delay",
        "risk_level": "Medium",
        "affected_products": "Product_061",
        "recommended_action": "Review downstream inventory requirements"
    }
]


for i, d in enumerate(pd.date_range("2026-07-07", "2026-07-17")):
    event = container_events[i % len(container_events)].copy()
    event["date"] = d.date()
    rows.append(event)

df = pd.DataFrame(rows)

print(df.head())

# Fabric example:
spark.createDataFrame(df).write.mode('overwrite').format('delta').saveAsTable('container_status')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Port Disruptions

# CELL ********************

# Generate port_disruptions

rows = []

port_events = [
    {
        "port_name": "Los Angeles",
        "country": "United States",
        "affected_warehouse": "WH_PHX",
        "disruption_type": "Port Congestion",
        "severity": "High",
        "status": "Active",
        "description": "High container volumes are causing vessel waiting times and terminal congestion.",
        "estimated_delay_days": 5,
        "affected_container_volume": 350,
        "affected_operations": "Vessel unloading and container pickup",
        "recommended_action": "Prioritize critical containers and evaluate alternate ports"
    },
    {
        "port_name": "Long Beach",
        "country": "United States",
        "affected_warehouse": "WH_LAX",
        "disruption_type": "Labor Constraints",
        "severity": "Medium",
        "status": "Monitoring",
        "description": "Reduced terminal productivity due to labor availability issues.",
        "estimated_delay_days": 3,
        "affected_container_volume": 180,
        "affected_operations": "Container handling and gate operations",
        "recommended_action": "Monitor terminal performance and adjust ETAs"
    },
    {
        "port_name": "Houston",
        "country": "United States",
        "affected_warehouse": "WH_DAL",
        "disruption_type": "Weather Event",
        "severity": "Critical",
        "status": "Active",
        "description": "Severe storms temporarily reduced port operations and vessel movements.",
        "estimated_delay_days": 7,
        "affected_container_volume": 420,
        "affected_operations": "Vessel arrivals, loading and unloading",
        "recommended_action": "Assess rerouting options and update shipment forecasts"
    },
    {
        "port_name": "New York",
        "country": "United States",
        "affected_warehouse": "WH_NYC",
        "disruption_type": "Customs Delays",
        "severity": "Medium",
        "status": "Monitoring",
        "description": "Increased customs inspection rates are slowing cargo release.",
        "estimated_delay_days": 4,
        "affected_container_volume": 120,
        "affected_operations": "Container clearance and delivery scheduling",
        "recommended_action": "Validate documentation completeness"
    },
    {
        "port_name": "Seattle",
        "country": "United States",
        "affected_warehouse": "WH_PHX",
        "disruption_type": "Equipment Shortage",
        "severity": "Low",
        "status": "Resolved",
        "description": "Temporary shortage of chassis equipment impacted container movement.",
        "estimated_delay_days": 1,
        "affected_container_volume": 60,
        "affected_operations": "Container pickup",
        "recommended_action": "Continue normal operations"
    },
    {
        "port_name": "Vancouver",
        "country": "Canada",
        "affected_warehouse": "WH_PHX",
        "disruption_type": "Severe Weather",
        "severity": "High",
        "status": "Active",
        "description": "Heavy rain and strong winds affected vessel schedules and terminal operations.",
        "estimated_delay_days": 6,
        "affected_container_volume": 260,
        "affected_operations": "Vessel berthing and container unloading",
        "recommended_action": "Review shipments from Asia and evaluate alternate routing"
    },
    {
        "port_name": "Los Angeles",
        "country": "United States",
        "affected_warehouse": "WH_PHX",
        "disruption_type": "Rail Capacity Constraint",
        "severity": "Medium",
        "status": "Monitoring",
        "description": "Limited rail availability is affecting inland container transportation.",
        "estimated_delay_days": 3,
        "affected_container_volume": 150,
        "affected_operations": "Rail transfer and inland transportation",
        "recommended_action": "Consider alternative trucking capacity"
    },
    {
        "port_name": "Long Beach",
        "country": "United States",
        "affected_warehouse": "WH_LAX",
        "disruption_type": "Terminal Maintenance",
        "severity": "Low",
        "status": "Resolved",
        "description": "Scheduled terminal maintenance temporarily reduced throughput.",
        "estimated_delay_days": 2,
        "affected_container_volume": 80,
        "affected_operations": "Container processing",
        "recommended_action": "No additional action required"
    },
    {
        "port_name": "Houston",
        "country": "United States",
        "affected_warehouse": "WH_DAL",
        "disruption_type": "Channel Restriction",
        "severity": "High",
        "status": "Monitoring",
        "description": "Temporary channel restrictions reduced vessel arrival capacity.",
        "estimated_delay_days": 5,
        "affected_container_volume": 220,
        "affected_operations": "Vessel arrivals",
        "recommended_action": "Monitor vessel schedules closely"
    },
    {
        "port_name": "New York",
        "country": "United States",
        "affected_warehouse": "WH_NYC",
        "disruption_type": "Truck Capacity",
        "severity": "Medium",
        "status": "Active",
        "description": "Regional trucking capacity shortage is delaying container pickup.",
        "estimated_delay_days": 3,
        "affected_container_volume": 140,
        "affected_operations": "Last-mile transportation",
        "recommended_action": "Secure alternative transportation providers"
    },
    {
        "port_name": "Seattle",
        "country": "United States",
        "affected_warehouse": "WH_PHX",
        "disruption_type": "Weather Event",
        "severity": "Low",
        "status": "Monitoring",
        "description": "Heavy rain may slow terminal operations temporarily.",
        "estimated_delay_days": 1,
        "affected_container_volume": 50,
        "affected_operations": "Container handling",
        "recommended_action": "Continue monitoring"
    }
]


for i, d in enumerate(pd.date_range("2026-07-07", "2026-07-17")):
    event = port_events[i % len(port_events)].copy()
    event["date"] = d.date()
    rows.append(event)

df = pd.DataFrame(rows)

print(df.head())

# Fabric example:
spark.createDataFrame(df).write.mode('overwrite').format('delta').saveAsTable('port_disruptions')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # Supply chain snapshot  
# This will serve as the entry point for many of the user queries the agent needs to investigate. If necessary, it investigates further the other tables, but only the ones necessary.

# CELL ********************

# -------------------------------------------------------
# Daily Supply Chain Snapshot
# One row per day
# July 6 - July 17, 2026
# -------------------------------------------------------

import pandas as pd

snapshot = pd.DataFrame([

{
    "date":"2026-07-06",
    "overall_otif":98.5,
    "overall_fill_rate":99.2,
    "forecast_accuracy":95.1,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":1,
    "high_priority_emails":0,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":8,
    "overall_status":"Healthy"
},

{
    "date":"2026-07-07",
    "overall_otif":98.4,
    "overall_fill_rate":99.0,
    "forecast_accuracy":94.8,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":1,
    "delayed_orders":2,
    "high_priority_emails":1,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":18,
    "overall_status":"Watch"
},

{
    "date":"2026-07-08",
    "overall_otif":98.0,
    "overall_fill_rate":98.5,
    "forecast_accuracy":91.5,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":2,
    "delayed_orders":4,
    "high_priority_emails":2,
    "supplier_issues":0,
    "weather_alerts":1,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":34,
    "overall_status":"Watch"
},

{
    "date":"2026-07-09",
    "overall_otif":97.2,
    "overall_fill_rate":97.8,
    "forecast_accuracy":90.2,
    "critical_inventory_items":2,
    "inventory_below_safety_stock":2,
    "delayed_orders":9,
    "high_priority_emails":3,
    "supplier_issues":0,
    "weather_alerts":1,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":55,
    "overall_status":"At Risk"
},

{
    "date":"2026-07-10",
    "overall_otif":96.3,
    "overall_fill_rate":96.9,
    "forecast_accuracy":89.0,
    "critical_inventory_items":2,
    "inventory_below_safety_stock":2,
    "delayed_orders":15,
    "high_priority_emails":3,
    "supplier_issues":0,
    "weather_alerts":1,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":72,
    "overall_status":"Critical"
},

{
    "date":"2026-07-11",
    "overall_otif":95.9,
    "overall_fill_rate":96.4,
    "forecast_accuracy":89.3,
    "critical_inventory_items":2,
    "inventory_below_safety_stock":2,
    "delayed_orders":17,
    "high_priority_emails":2,
    "supplier_issues":0,
    "weather_alerts":1,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":76,
    "overall_status":"Critical"
},

{
    "date":"2026-07-12",
    "overall_otif":97.1,
    "overall_fill_rate":97.8,
    "forecast_accuracy":91.2,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":8,
    "high_priority_emails":1,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":38,
    "overall_status":"Recovering"
},

{
    "date":"2026-07-13",
    "overall_otif":98.2,
    "overall_fill_rate":99.0,
    "forecast_accuracy":95.4,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":2,
    "high_priority_emails":0,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":12,
    "overall_status":"Healthy"
},

{
    "date":"2026-07-14",
    "overall_otif":98.4,
    "overall_fill_rate":99.1,
    "forecast_accuracy":96.0,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":1,
    "high_priority_emails":1,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":10,
    "overall_status":"Healthy"
},

{
    "date":"2026-07-15",
    "overall_otif":98.6,
    "overall_fill_rate":99.2,
    "forecast_accuracy":96.3,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":1,
    "high_priority_emails":0,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":8,
    "overall_status":"Healthy"
},

{
    "date":"2026-07-16",
    "overall_otif":98.7,
    "overall_fill_rate":99.3,
    "forecast_accuracy":96.5,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":0,
    "high_priority_emails":0,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":6,
    "overall_status":"Healthy"
},

{
    "date":"2026-07-17",
    "overall_otif":98.8,
    "overall_fill_rate":99.4,
    "forecast_accuracy":96.7,
    "critical_inventory_items":0,
    "inventory_below_safety_stock":0,
    "delayed_orders":0,
    "high_priority_emails":0,
    "supplier_issues":0,
    "weather_alerts":0,
    "container_delays":0,
    "port_disruptions":0,
    "overall_risk_score":5,
    "overall_status":"Healthy"
}

])

snapshot["date"] = pd.to_datetime(snapshot["date"])

display(snapshot)

# Fabric
spark.createDataFrame(snapshot)\
    .write.mode("overwrite")\
    .format("delta")\
    .saveAsTable("daily_supply_chain_snapshot")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
