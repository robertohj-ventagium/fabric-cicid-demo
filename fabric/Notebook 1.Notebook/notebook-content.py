# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
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
# META     },
# META     "mirrored_db": {
# META       "known_mirrored_dbs": [
# META         {
# META           "id": "376e6d49-4021-4996-aa78-6124427a2294"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import pandas as pd
# Load data into pandas DataFrame from "/lakehouse/default/Files/dbo.FactFinance.csv"
df = pd.read_csv("/lakehouse/default/Files/dbo.FactFinance.csv")
display(df)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pyodbc
import struct
from notebookutils import credentials

server = "6unlohtqbrpuleev5bpjprytom-hey6wg25fszuznawyrsaivk3je.database.fabric.microsoft.com"
database = "Adventure_Works_DW_2017-376e6d49-4021-4996-aa78-6124427a2294"

# Obtener token para Azure SQL
token = credentials.getToken("https://database.windows.net/")

# Convertir al formato requerido por pyodbc
token_bytes = token.encode("utf-16-le")
token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pyodbc
import struct
from notebookutils import credentials

server = "6unlohtqbrpuleev5bpjprytom-hey6wg25fszuznawyrsaivk3je.database.fabric.microsoft.com"
database = "Adventure_Works_DW_2017-376e6d49-4021-4996-aa78-6124427a2294"

token = credentials.getToken("https://database.windows.net/")

token_bytes = token.encode("utf-16-le")
token_struct = struct.pack(
    f"<I{len(token_bytes)}s",
    len(token_bytes),
    token_bytes
)

SQL_COPT_SS_ACCESS_TOKEN = 1256

conn = pyodbc.connect(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={server},1433;"
    f"Database={database};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;",
    attrs_before={
        SQL_COPT_SS_ACCESS_TOKEN: token_struct
    },
    timeout=60
)

cursor = conn.cursor()

cursor.execute("SELECT 1")
print(cursor.fetchone())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df = df.where(df.notna(), None)

print(df.dtypes)
print(df.head())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Example INSERT
cursor.fast_executemany = True

query = """
INSERT INTO dbo.FactFinance
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(
    query,
    df.values.tolist()
)

conn.commit()

print("Data inserted successfully.")

cursor.close()
conn.close()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Load data into pandas DataFrame from "/lakehouse/default/Files/dbo.DimAccount.csv"
df2 = pd.read_csv("/lakehouse/default/Files/dbo.DimAccount.csv")
display(df2)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Example INSERT
cursor.fast_executemany = True

query = """
INSERT INTO dbo.DimAccount
(
   AccountKey,
   ParentAccountKey,
   AccountCodeAlternateKey,
   ParentAccountCodeAlternateKey,
   AccountDescription,
   AccountType,
   Operator,
   CustomMembers,
   ValueType,
   CustomMemberOptions
    )
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(
    query,
    df2.values.tolist()
)

conn.commit()

print("Data inserted successfully.")

cursor.close()
conn.close()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pandas as pd
import numpy as np

df2 = df2.astype(object)
df2 = df2.where(pd.notnull(df2), None)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pandas as pd
df3 = pd.read_csv("/lakehouse/default/Files/dbo.DimDate.csv")
display(df3)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pyodbc
import struct
from notebookutils import credentials

server = "6unlohtqbrpuleev5bpjprytom-hey6wg25fszuznawyrsaivk3je.database.fabric.microsoft.com"
database = "Adventure_Works_DW_2017-376e6d49-4021-4996-aa78-6124427a2294"

# Obtener token para Azure SQL
token = credentials.getToken("https://database.windows.net/")

# Convertir al formato requerido por pyodbc
token_bytes = token.encode("utf-16-le")
token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

import pyodbc
import struct
from notebookutils import credentials

server = "6unlohtqbrpuleev5bpjprytom-hey6wg25fszuznawyrsaivk3je.database.fabric.microsoft.com"
database = "Adventure_Works_DW_2017-376e6d49-4021-4996-aa78-6124427a2294"

token = credentials.getToken("https://database.windows.net/")

token_bytes = token.encode("utf-16-le")
token_struct = struct.pack(
    f"<I{len(token_bytes)}s",
    len(token_bytes),
    token_bytes
)

SQL_COPT_SS_ACCESS_TOKEN = 1256

conn = pyodbc.connect(
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={server},1433;"
    f"Database={database};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;",
    attrs_before={
        SQL_COPT_SS_ACCESS_TOKEN: token_struct
    },
    timeout=60
)

cursor = conn.cursor()

cursor.execute("SELECT 1")
print(cursor.fetchone())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df3['FullDateAlternateKey'] = pd.to_datetime(df3['FullDateAlternateKey'], format = '%d/%m/%Y')
df3['FullDateAlternateKey'].dtype

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

# Example INSERT
cursor.fast_executemany = True

query = """
INSERT INTO dbo.DimDate
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

cursor.executemany(
    query,
    df3.values.tolist()
)

conn.commit()

print("Data inserted successfully.")

cursor.close()
conn.close()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

df3.dtypes

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
