# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0a848f75-e579-4c5a-ad38-1c9ed640dff2",
# META       "default_lakehouse_name": "Dynamic_Metrics_Lakehouse",
# META       "default_lakehouse_workspace_id": "1beb3139-2c5d-4cb3-b416-c46404555b49",
# META       "known_lakehouses": [
# META         {
# META           "id": "0a848f75-e579-4c5a-ad38-1c9ed640dff2"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Dynamic Metrics Overview — Stage 0 data seed
# 
# Writes the four curated Delta tables that back the Dynamic Metrics Overview semantic model:
# 
# | Table | Grain |
# | --- | --- |
# | `Department` | one row per department |
# | `Category` | one row per category |
# | `Metric` | one row per metric |
# | `MetricValue` | one row per metric / month |
# 
# ## How to run
# 
# 1. Import this notebook into the Fabric workspace.
# 2. Attach the target lakehouse as the notebook's **default lakehouse** (Explorer → Add lakehouse).
# 3. **Run all**.
# 
# The generated data is fully deterministic — there is no random number generation, so every run
# produces identical rows and the semantic model stays reproducible.

# CELL ********************

import math
from datetime import date

from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

# 15 monthly observations per metric, most recent = 2026-08.
MONTHS = 15
LAST_PERIOD = (2026, 8)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Reference data
# 
# The hierarchy lives here and nowhere else — the application never hardcodes these names.

# CELL ********************

DEPARTMENTS = [
    (1, 'Operations'),
    (2, 'Finance'),
    (3, 'Customer'),
    (4, 'People'),
    (5, 'Technology'),
]

CATEGORIES = [
    (11, 'Supply Chain', 1),
    (12, 'Manufacturing', 1),
    (21, 'Revenue', 2),
    (22, 'Cost Management', 2),
    (23, 'Profitability', 2),
    (31, 'Satisfaction', 3),
    (32, 'Retention', 3),
    (41, 'Talent Acquisition', 4),
    (42, 'Engagement', 4),
    (43, 'Learning and Development', 4),
    (51, 'Platform Reliability', 5),
    (52, 'Information Security', 5),
    (53, 'Software Delivery', 5),
]

# (id, name, category_id, description, unit, target, higher_is_better,
#  latest_value, monthly_step, wobble, decimals)
METRICS = [
    (101, 'On-Time Delivery Rate', 11,
     'Share of customer orders delivered on or before the promised date.',
     '%', 95.0, True, 96.4, 0.18, 0.60, 1),
    (102, 'Inventory Turnover', 11,
     'Number of times average inventory is sold and replaced per year.',
     'turns', 8.0, True, 7.5, 0.04, 0.25, 2),
    (103, 'Order Fulfillment Rate', 11,
     'Share of order lines shipped complete from available stock.',
     '%', 98.0, True, 98.1, 0.06, 0.35, 1),
    (104, 'Production Efficiency', 12,
     'Actual output as a share of rated production capacity.',
     '%', 90.0, True, 92.3, 0.22, 0.70, 1),
    (105, 'Defect Rate', 12,
     'Share of manufactured units rejected by quality control.',
     '%', 1.50, False, 1.82, -0.03, 0.09, 2),
    (106, 'Monthly Revenue', 21,
     'Total recognised revenue for the month across all product lines.',
     'USD', 4500000.0, True, 4780000.0, 42000.0, 95000.0, 0),
    (107, 'Revenue Growth', 21,
     'Month-over-month change in recognised revenue.',
     '%', 5.0, True, 4.1, 0.05, 0.50, 1),
    (108, 'Operating Cost', 22,
     'Total operating expenditure recorded for the month.',
     'USD', 3200000.0, False, 3145000.0, -12000.0, 55000.0, 0),
    (109, 'Cost Variance', 22,
     'Deviation of actual operating cost from the approved budget.',
     '%', 2.0, False, 1.9, -0.06, 0.40, 1),
    (110, 'Gross Margin', 23,
     'Gross profit as a share of revenue.',
     '%', 42.0, True, 43.6, 0.12, 0.45, 1),
    (111, 'Operating Margin', 23,
     'Operating profit as a share of revenue.',
     '%', 18.0, True, 17.8, 0.07, 0.40, 1),
    (112, 'Customer Satisfaction Score', 31,
     'Average post-interaction customer satisfaction rating, scale 1-5.',
     'score', 4.5, True, 4.42, 0.012, 0.05, 2),
    (113, 'Net Promoter Score', 31,
     'Promoters minus detractors from the monthly relationship survey.',
     'score', 45.0, True, 48.0, 0.55, 1.60, 0),
    (114, 'Customer Retention Rate', 32,
     'Share of active customers retained over a rolling twelve months.',
     '%', 92.0, True, 90.6, 0.10, 0.50, 1),
    (115, 'Churn Rate', 32,
     'Share of customers who cancelled during the month.',
     '%', 3.0, False, 2.7, -0.03, 0.15, 2),
    (116, 'Average Resolution Time', 32,
     'Mean time to resolve an escalated customer support case.',
     'hours', 4.0, False, 4.6, -0.05, 0.22, 2),
    (117, 'Time to Hire', 41,
     'Average calendar days from approved requisition to accepted offer.',
     'days', 30.0, False, 32.5, -0.25, 0.80, 1),
    (118, 'Offer Acceptance Rate', 41,
     'Share of extended offers accepted by candidates.',
     '%', 85.0, True, 87.2, 0.20, 0.90, 1),
    (119, 'Employee Engagement Score', 42,
     'Average engagement rating from the monthly employee pulse survey, scale 1-5.',
     'score', 4.20, True, 4.05, 0.015, 0.05, 2),
    (120, 'Voluntary Attrition Rate', 42,
     'Share of employees leaving voluntarily over a rolling twelve months.',
     '%', 10.0, False, 11.4, -0.06, 0.30, 1),
    (121, 'Absenteeism Rate', 42,
     'Share of scheduled working days lost to unplanned absence.',
     '%', 2.50, False, 2.44, -0.02, 0.12, 2),
    (122, 'Training Completion Rate', 43,
     'Share of assigned training courses completed by their due date.',
     '%', 90.0, True, 93.1, 0.35, 1.10, 1),
    (123, 'Training Hours per Employee', 43,
     'Average formal learning hours delivered per employee per quarter.',
     'hours', 20.0, True, 18.6, 0.12, 0.70, 1),
    (124, 'System Uptime', 51,
     'Share of time core platform services were available to users.',
     '%', 99.90, True, 99.94, 0.004, 0.03, 2),
    (125, 'Mean Time to Recovery', 51,
     'Average time to restore service after a production incident.',
     'hours', 2.00, False, 2.35, -0.03, 0.10, 2),
    (126, 'Incident Volume', 51,
     'Number of production incidents raised during the month.',
     'incidents', 25.0, False, 21.0, -0.45, 1.80, 0),
    (127, 'Critical Vulnerability Backlog', 52,
     'Open critical security vulnerabilities past their remediation deadline.',
     'issues', 5.0, False, 6.0, -0.30, 1.20, 0),
    (128, 'Patch Compliance Rate', 52,
     'Share of managed endpoints patched within the required window.',
     '%', 95.0, True, 96.3, 0.25, 0.80, 1),
    (129, 'Deployment Frequency', 53,
     'Number of production deployments completed during the month.',
     'deployments', 40.0, True, 46.0, 0.70, 2.50, 0),
    (130, 'Change Failure Rate', 53,
     'Share of production deployments requiring a rollback or hotfix.',
     '%', 15.0, False, 13.8, -0.20, 0.60, 1),
]

print(f'{len(DEPARTMENTS)} departments, {len(CATEGORIES)} categories, {len(METRICS)} metrics')


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Deterministic history
# 
# Each observation walks backwards from the metric's latest value using a fixed monthly step plus a
# fixed sine wobble, so every series has a visible trend and month-to-month movement without any
# randomness.

# CELL ********************

def slug(name):
    return name.lower().replace(' ', '-')


def month_series(months, last_period):
    '''Ordered list of first-of-month dates ending at last_period.'''
    year, month = last_period
    periods = []
    for _ in range(months):
        periods.append(date(year, month, 1))
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    return list(reversed(periods))


def observation(index, metric):
    '''Deterministic value for the metric at position index (0 = oldest).'''
    metric_id, _, _, _, _, _, _, latest, step, wobble, decimals = metric
    offset = MONTHS - 1 - index
    phase = (metric_id % 7) * 0.45
    seasonal = wobble * math.sin(index * 0.9 + phase)
    value = latest - step * offset + seasonal
    return round(value, decimals) if decimals > 0 else float(round(value))


periods = month_series(MONTHS, LAST_PERIOD)
print(f'{len(periods)} periods: {periods[0]} .. {periods[-1]}')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

department_rows = [(dept_id, name) for dept_id, name in DEPARTMENTS]

category_rows = [(cat_id, name, dept_id) for cat_id, name, dept_id in CATEGORIES]

metric_rows = [
    (
        metric[0],
        metric[1],
        metric[2],
        metric[3],
        metric[4],
        float(metric[5]),
        metric[6],
        'https://example.com/metrics/' + slug(metric[1]),
    )
    for metric in METRICS
]

metric_value_rows = [
    (metric[0], period, observation(index, metric))
    for metric in METRICS
    for index, period in enumerate(periods)
]

print(f'{len(metric_value_rows)} metric observations')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Write the Delta tables
# 
# Tables are written to the notebook's **default lakehouse** with `overwrite`, so re-running is
# idempotent.

# CELL ********************

department_schema = StructType([
    StructField('DepartmentID', IntegerType(), False),
    StructField('DepartmentName', StringType(), False),
])

category_schema = StructType([
    StructField('CategoryID', IntegerType(), False),
    StructField('CategoryName', StringType(), False),
    StructField('DepartmentID', IntegerType(), False),
])

metric_schema = StructType([
    StructField('MetricID', IntegerType(), False),
    StructField('MetricName', StringType(), False),
    StructField('CategoryID', IntegerType(), False),
    StructField('MetricDescription', StringType(), False),
    StructField('Unit', StringType(), False),
    StructField('TargetValue', DoubleType(), False),
    StructField('HigherIsBetter', BooleanType(), False),
    StructField('DetailURL', StringType(), False),
])

metric_value_schema = StructType([
    StructField('MetricID', IntegerType(), False),
    StructField('Date', DateType(), False),
    StructField('Value', DoubleType(), False),
])

tables = [
    ('Department', department_rows, department_schema),
    ('Category', category_rows, category_schema),
    ('Metric', metric_rows, metric_schema),
    ('MetricValue', metric_value_rows, metric_value_schema),
]

for table_name, rows, schema in tables:
    df = spark.createDataFrame(rows, schema=schema)
    (
        df.write.format('delta')
        .mode('overwrite')
        .option('overwriteSchema', 'true')
        .saveAsTable(table_name)
    )
    print(f'{table_name}: {df.count()} rows written')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Referential integrity
# 
# The model must contain no orphaned categories, metrics or observations.

# CELL ********************

departments = spark.read.table('Department')
categories = spark.read.table('Category')
metrics = spark.read.table('Metric')
values = spark.read.table('MetricValue')

orphan_categories = categories.join(departments, 'DepartmentID', 'left_anti').count()
orphan_metrics = metrics.join(categories, 'CategoryID', 'left_anti').count()
orphan_values = values.join(metrics, 'MetricID', 'left_anti').count()

print(f'orphans -> categories: {orphan_categories}, metrics: {orphan_metrics}, values: {orphan_values}')
assert orphan_categories == 0 and orphan_metrics == 0 and orphan_values == 0

assert metrics.select('MetricID').distinct().count() == metrics.count()
assert metrics.select('MetricName').distinct().count() == metrics.count()

min_observations = values.groupBy('MetricID').count().agg({'count': 'min'}).collect()[0][0]
print(f'minimum observations per metric: {min_observations}')
assert min_observations >= 12

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Preview the hierarchy

# CELL ********************

hierarchy = (
    metrics.join(categories, 'CategoryID')
    .join(departments, 'DepartmentID')
    .select(
        'DepartmentName',
        'CategoryName',
        'MetricName',
        'Unit',
        'TargetValue',
        'DetailURL',
    )
    .orderBy('DepartmentName', 'CategoryName', 'MetricName')
)

display(hierarchy)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM Dynamic_Metrics_Lakehouse.Metric LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
