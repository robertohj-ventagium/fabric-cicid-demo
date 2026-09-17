# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "a47a5921-a371-4f6b-8ecc-b96d44023928",
# META       "default_lakehouse_name": "Static_Metrics_Lakehouse",
# META       "default_lakehouse_workspace_id": "1beb3139-2c5d-4cb3-b416-c46404555b49",
# META       "known_lakehouses": [
# META         {
# META           "id": "a47a5921-a371-4f6b-8ecc-b96d44023928"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Static Metrics Report — Stage 0 data seed
# 
# Writes the curated Delta tables that back the **static Power BI Metrics Report**.
# 
# The data definitions and deterministic monthly metric history are intentionally the same as the
# Dynamic Metrics Overview seed. The difference is the physical model: shared dimensions live in
# `dbo`, while each department gets its own `Metric` and `MetricValue` tables.
# 
# | Schema | Tables |
# | --- | --- |
# | `dbo` | `Department`, `Category`, `Calendar` |
# | `operations` | `Metric`, `MetricValue` |
# | `finance` | `Metric`, `MetricValue` |
# | `customer` | `Metric`, `MetricValue` |
# | `people` | `Metric`, `MetricValue` |
# | `technology` | `Metric`, `MetricValue` |
# 
# ## How to run
# 
# 1. Import this notebook into the Fabric workspace.
# 2. Attach the target lakehouse as the notebook's **default lakehouse** (Explorer → Add lakehouse).
# 3. **Run all**.
# 
# The generated data is fully deterministic. Re-running the notebook overwrites the curated tables,
# so the result is reproducible and does not accumulate duplicate rows.


# CELL ********************

import math
from calendar import monthrange
from datetime import date, timedelta

from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

# Same history as the Dynamic Metrics Overview.
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
# These definitions are copied from the Dynamic Metrics Overview seed so both demos use the same
# business data. Metrics are later distributed to department-specific schemas based on their category.


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

# ## Deterministic history and calendar
# 
# Each metric follows the same deterministic monthly history used by the dynamic scenario.
# The shared `dbo.Calendar` is a daily calendar covering the full reporting period.


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

def calendar_series(first_period, last_period):
    start = date(first_period[0], first_period[1], 1)
    end_day = monthrange(last_period[0], last_period[1])[1]
    end = date(last_period[0], last_period[1], end_day)

    rows = []
    current = start
    while current <= end:
        rows.append((
            current,
            current.year,
            current.month,
            current.strftime('%B'),
            current.strftime('%Y-%m'),
        ))
        current += timedelta(days=1)
    return rows


calendar_rows = calendar_series((periods[0].year, periods[0].month), LAST_PERIOD)

print(f'{len(periods)} metric periods: {periods[0]} .. {periods[-1]}')
print(f'{len(calendar_rows)} calendar dates: {calendar_rows[0][0]} .. {calendar_rows[-1][0]}')


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Prepare department-specific rows
# 
# `Department` and `Category` remain shared in `dbo`.
# 
# Each department receives only its own metrics and metric observations. The same `MetricID` values
# are retained from the dynamic scenario; only the physical table/schema changes.


# CELL ********************

department_rows = [(dept_id, name) for dept_id, name in DEPARTMENTS]

category_rows = [(cat_id, name, dept_id) for cat_id, name, dept_id in CATEGORIES]

category_to_department = {cat_id: dept_id for cat_id, _, dept_id in CATEGORIES}
department_to_schema = {
    1: 'operations',
    2: 'finance',
    3: 'customer',
    4: 'people',
    5: 'technology',
}

# Preserve the same metric columns as the dynamic model.
metric_rows_by_department = {schema: [] for schema in department_to_schema.values()}
metric_value_rows_by_department = {schema: [] for schema in department_to_schema.values()}

for metric in METRICS:
    metric_id, metric_name, category_id, description, unit, target, higher_is_better, *_ = metric
    department_id = category_to_department[category_id]
    schema_name = department_to_schema[department_id]

    metric_rows_by_department[schema_name].append((
        metric_id,
        metric_name,
        category_id,
        description,
        unit,
        float(target),
        higher_is_better,
        'https://example.com/metrics/' + slug(metric_name),
    ))

    for index, period in enumerate(periods):
        metric_value_rows_by_department[schema_name].append(
            (metric_id, period, observation(index, metric))
        )

for schema_name in department_to_schema.values():
    print(
        f'{schema_name}: '
        f'{len(metric_rows_by_department[schema_name])} metrics, '
        f'{len(metric_value_rows_by_department[schema_name])} observations'
    )


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Write the Delta tables
# 
# The target lakehouse is the notebook's **default lakehouse**. No workspace or lakehouse IDs are
# hard-coded.
# 
# The department schemas are created if they do not already exist.


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

calendar_schema = StructType([
    StructField('Date', DateType(), False),
    StructField('Year', IntegerType(), False),
    StructField('MonthNumber', IntegerType(), False),
    StructField('MonthName', StringType(), False),
    StructField('YearMonth', StringType(), False),
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

for schema_name in department_to_schema.values():
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{schema_name}`")

shared_tables = [
    ('dbo.Department', department_rows, department_schema),
    ('dbo.Category', category_rows, category_schema),
    ('dbo.Calendar', calendar_rows, calendar_schema),
]

for table_name, rows, schema in shared_tables:
    df = spark.createDataFrame(rows, schema=schema)
    (
        df.write.format('delta')
        .mode('overwrite')
        .option('overwriteSchema', 'true')
        .saveAsTable(table_name)
    )
    print(f'{table_name}: {df.count()} rows written')

for schema_name in department_to_schema.values():
    metric_df = spark.createDataFrame(
        metric_rows_by_department[schema_name],
        schema=metric_schema,
    )
    value_df = spark.createDataFrame(
        metric_value_rows_by_department[schema_name],
        schema=metric_value_schema,
    )

    (
        metric_df.write.format('delta')
        .mode('overwrite')
        .option('overwriteSchema', 'true')
        .saveAsTable(f'{schema_name}.Metric')
    )

    (
        value_df.write.format('delta')
        .mode('overwrite')
        .option('overwriteSchema', 'true')
        .saveAsTable(f'{schema_name}.MetricValue')
    )

    print(
        f'{schema_name}.Metric: {metric_df.count()} rows written | '
        f'{schema_name}.MetricValue: {value_df.count()} rows written'
    )


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Referential integrity and coverage
# 
# Validate the shared hierarchy, then validate each department's metric and observation tables.
# The checks also ensure every metric has the full 15-month history.


# CELL ********************

departments = spark.read.table('dbo.Department')
categories = spark.read.table('dbo.Category')

orphan_categories = categories.join(
    departments, 'DepartmentID', 'left_anti'
).count()

assert orphan_categories == 0

total_metrics = 0
total_observations = 0

for department_id, department_name in DEPARTMENTS:
    schema_name = department_to_schema[department_id]
    metrics = spark.read.table(f'{schema_name}.Metric')
    values = spark.read.table(f'{schema_name}.MetricValue')

    # Metrics must belong to a category owned by this department.
    department_categories = categories.filter(
        categories.DepartmentID == department_id
    )
    orphan_metrics = metrics.join(
        department_categories, 'CategoryID', 'left_anti'
    ).count()
    assert orphan_metrics == 0

    # Every observation must reference a metric in the same department.
    orphan_values = values.join(
        metrics, 'MetricID', 'left_anti'
    ).count()
    assert orphan_values == 0

    # IDs and names are unique within each department.
    assert metrics.select('MetricID').distinct().count() == metrics.count()
    assert metrics.select('MetricName').distinct().count() == metrics.count()

    min_observations = (
        values.groupBy('MetricID')
        .count()
        .agg({'count': 'min'})
        .collect()[0][0]
    )
    assert min_observations == MONTHS

    total_metrics += metrics.count()
    total_observations += values.count()

    print(
        f'{department_name}: '
        f'{metrics.count()} metrics, '
        f'{values.count()} observations, '
        f'min observations/metric = {min_observations}'
    )

assert total_metrics == len(METRICS)
assert total_observations == len(METRICS) * MONTHS

calendar = spark.read.table('dbo.Calendar')
assert calendar.select('Date').distinct().count() == calendar.count()

print(f'Total metrics: {total_metrics}')
print(f'Total observations: {total_observations}')
print(f'Calendar rows: {calendar.count()}')
print('All integrity checks passed.')


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Preview the static model
# 
# This preview combines the department-specific metric tables only for validation. The actual
# lakehouse remains physically separated by department schema.


# CELL ********************

from functools import reduce
from pyspark.sql import DataFrame

department_previews = []

for department_id, department_name in DEPARTMENTS:
    schema_name = department_to_schema[department_id]

    preview = (
        spark.read.table(f'{schema_name}.Metric')
        .join(categories, 'CategoryID')
        .join(departments, 'DepartmentID')
        .select(
            'DepartmentName',
            'CategoryName',
            'MetricName',
            'Unit',
            'TargetValue',
            'DetailURL',
        )
    )
    department_previews.append(preview)

hierarchy = reduce(DataFrame.unionByName, department_previews).orderBy(
    'DepartmentName', 'CategoryName', 'MetricName'
)

display(hierarchy)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
