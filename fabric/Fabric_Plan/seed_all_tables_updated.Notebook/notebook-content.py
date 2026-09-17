# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   }
# META }

# MARKDOWN ********************

# # Seed All Tables — Retail Forecast POC (small / international)
# Target: **SQL Database in Fabric** · Lenguaje: **Python** · **sin Spark** (todo en pandas)
# 
# Dataset pequeño para crearlo rápido. Datos en inglés y a nivel internacional.
# Ejecuta las celdas **una por una, en orden**. Solo editas `SERVER` y `DATABASE` en la Celda 1.
# 
# | Celda | Tabla | Filas aprox |
# |---|---|---|
# | 1 | config / auth (history + future horizon) | — |
# | 1.5–1.6 | `dim_date` (hasta FUTURE_END+1 mes) | ~900 |
# | 2 | `dim_store` | 20 |
# | 3 | `dim_product` | 100 |
# | 4 | lectura de llaves (history + future) | — |
# | 5 | `fact_actual_sales` (solo pasado) | ~150-200K |
# | 6 | `fact_forecast` (pasado + 6 meses futuros) | ~900K-1.1M |
# | 7 | `fact_planning_scenario` | ~30-60K |
# | 8 | verificación + MAPE | — |
# 
# **Tiempo total estimado: 6-10 min.** Sin Spark = sin problemas de token.

# MARKDOWN ********************

# ## Celda 1 — Config & conexión
# Edita las dos líneas marcadas. `make_engine()` crea un engine con token fresco; lo llamamos antes de cada carga para que nunca expire.

# CELL ********************

import struct
import numpy as np
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine, event, text
from notebookutils import credentials

# ── Edita solo estas dos líneas ──────────────────────────────────────────────
SERVER   = "6unlohtqbrpuleev5bpjprytom-hey6wg25fszuznawyrsaivk3je.database.fabric.microsoft.com"
DATABASE = "Test_Store_DB-1b247ee8-ca8c-4b17-8405-dcf0ac48a8b3"
# ─────────────────────────────────────────────────────────────────────────────

DRIVER = "ODBC Driver 18 for SQL Server"
SEED   = 42
RNG    = np.random.default_rng(SEED)

# Historia: últimos 12 meses (para actuals y MAPE)
# Futuro: próximos 6 meses (planning horizon — solo forecast, sin actuals)
DATE_END   = date.today()
DATE_START = DATE_END - relativedelta(months=12)
FUTURE_END = DATE_END + relativedelta(months=6)
print(f"History: {DATE_START} → {DATE_END} ({(DATE_END-DATE_START).days+1} días)")
print(f"Forecast horizon: {DATE_END} → {FUTURE_END} ({(FUTURE_END-DATE_END).days} días futuros)")

_conn_str = (
    f"Driver={{{DRIVER}}};Server={SERVER},1433;Database={DATABASE};"
    "Encrypt=Yes;TrustServerCertificate=No"
)

def make_engine():
    """Crea un SQLAlchemy engine con un token Entra ID recién obtenido."""
    tok   = credentials.getToken("https://database.windows.net/.default")
    tok_b = bytes(tok, "UTF-16-LE")
    tok_s = struct.pack(f"<I{len(tok_b)}s", len(tok_b), tok_b)
    eng   = create_engine(f"mssql+pyodbc:///?odbc_connect={_conn_str}", fast_executemany=True)
    @event.listens_for(eng, "do_connect")
    def _inject(dialect, conn_rec, cargs, cparams):
        cargs[0] = cargs[0].replace(";Trusted_Connection=Yes", "")
        cparams["attrs_before"] = {1256: tok_s}
    return eng

engine = make_engine()
print("Conexión configurada ✓")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 1.5 — generar `dim_date` (inglés, festivos internacionales)
# Nombres en inglés, festivos globales (incl. US Thanksgiving para anclar Black Friday) y temporadas retail internacionales.

# CELL ********************

from datetime import date, timedelta
from dateutil.easter import easter

DIM_DATE_START = "2025-01-01"
# Extiende hasta fin del mes siguiente al horizonte futuro, para cubrir todo el rango
DIM_DATE_END   = (FUTURE_END + relativedelta(months=1)).strftime("%Y-%m-%d")

DAY_NAMES_EN = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",
                4:"Friday",5:"Saturday",6:"Sunday"}
MONTH_NAMES_EN = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",
                  7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}

def nth_weekday(year, month, weekday, n):
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + 7 * (n - 1))

def thanksgiving(year):
    # US Thanksgiving = 4th Thursday of November (weekday 3)
    return nth_weekday(year, 11, 3, 4)

def classify_retail_season(d):
    # Back-to-School: Jul 15 - Sep 5
    if (d.month == 7 and d.day >= 15) or d.month == 8 or (d.month == 9 and d.day <= 5):
        return "Back-to-School"
    # Black Friday / Cyber: Thanksgiving through the following Monday (Cyber Monday)
    tg = thanksgiving(d.year)
    if tg <= d <= tg + timedelta(days=4):
        return "Black Friday"
    # Holiday: all of December
    if d.month == 12:
        return "Holiday"
    return "Regular"

def build_holiday_map(y0, y1):
    h = {}
    for y in range(y0, y1 + 1):
        h[date(y,1,1)]                   = "New Year's Day"
        h[easter(y) - timedelta(days=2)] = "Good Friday"
        h[easter(y) + timedelta(days=1)] = "Easter Monday"
        h[date(y,5,1)]                   = "Labour Day"
        h[thanksgiving(y)]               = "Thanksgiving"
        h[date(y,12,24)]                 = "Christmas Eve"
        h[date(y,12,25)]                 = "Christmas Day"
        h[date(y,12,26)]                 = "Boxing Day"
        h[date(y,12,31)]                 = "New Year's Eve"
    return h

dates = pd.date_range(start=DIM_DATE_START, end=DIM_DATE_END, freq="D")
dd = pd.DataFrame({"_dt": dates})
dd["DateKey"]       = dd["_dt"].dt.strftime("%Y%m%d").astype(int)
dd["Date"]          = dd["_dt"].dt.date
dd["DayOfWeek"]     = dd["_dt"].dt.dayofweek + 1
dd["DayName"]       = dd["_dt"].dt.dayofweek.map(DAY_NAMES_EN)
dd["WeekNumber"]    = dd["_dt"].dt.isocalendar().week.astype(int)
dd["WeekStartDate"] = (dd["_dt"] - pd.to_timedelta(dd["_dt"].dt.dayofweek, unit="D")).dt.date
dd["MonthNumber"]   = dd["_dt"].dt.month
dd["MonthName"]     = dd["_dt"].dt.month.map(MONTH_NAMES_EN)
dd["MonthYear"]     = dd["_dt"].dt.strftime("%Y-%m")
dd["Quarter"]       = dd["_dt"].dt.quarter
dd["Year"]          = dd["_dt"].dt.year
dd["FiscalPeriod"]  = dd["MonthNumber"]
dd["FiscalQuarter"] = dd["Quarter"]
dd["FiscalYear"]    = dd["Year"]
dd["IsWeekend"]     = dd["DayOfWeek"].isin([6, 7]).astype(int)

hol = build_holiday_map(int(DIM_DATE_START[:4]), int(DIM_DATE_END[:4]))
dd["IsHoliday"]    = dd["Date"].map(lambda d: d in hol).astype(int)
dd["HolidayName"]  = dd["Date"].map(hol)
dd["RetailSeason"] = dd["Date"].map(classify_retail_season)

dd = dd[["DateKey","Date","DayOfWeek","DayName","WeekNumber","WeekStartDate",
         "MonthNumber","MonthName","MonthYear","Quarter","Year",
         "FiscalPeriod","FiscalQuarter","FiscalYear",
         "IsWeekend","IsHoliday","HolidayName","RetailSeason"]]

print(f"Generated {len(dd):,} rows ({dd['Date'].min()} → {dd['Date'].max()})")
print(f"Holidays: {int(dd['IsHoliday'].sum())}  |  Seasons: {dd['RetailSeason'].value_counts().to_dict()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 1.6 — cargar `dim_date`

# CELL ********************

eng = make_engine()
with eng.begin() as conn:
    conn.execute(text("DELETE FROM dbo.dim_date"))   # DELETE respeta las FKs
dd.to_sql("dim_date", eng, schema="dbo", if_exists="append", index=False, chunksize=500)
print(f"dim_date: {len(dd):,} filas cargadas ✓")
print(pd.read_sql("SELECT COUNT(*) n, MIN([Date]) min_d, MAX([Date]) max_d FROM dbo.dim_date",
                  eng).to_string(index=False))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 2 — `dim_store` (20 tiendas, internacional)
# 4 regiones: North America, Europe, APAC, LATAM. Países y ciudades reales.

# CELL ********************

# (Region, Country, State/Province, City) — 20 ubicaciones internacionales
STORE_LOCATIONS = [
    ("North America", "United States", "New York",          "New York City"),
    ("North America", "United States", "California",        "Los Angeles"),
    ("North America", "United States", "Illinois",          "Chicago"),
    ("North America", "United States", "Texas",             "Houston"),
    ("North America", "Canada",        "Ontario",           "Toronto"),
    ("North America", "Canada",        "British Columbia",  "Vancouver"),
    ("Europe",        "United Kingdom","England",           "London"),
    ("Europe",        "United Kingdom","England",           "Manchester"),
    ("Europe",        "Germany",       "Bavaria",           "Munich"),
    ("Europe",        "Germany",       "Berlin",            "Berlin"),
    ("Europe",        "France",        "Île-de-France",     "Paris"),
    ("Europe",        "Spain",         "Catalonia",         "Barcelona"),
    ("APAC",          "Japan",         "Tokyo",             "Tokyo"),
    ("APAC",          "Japan",         "Osaka",             "Osaka"),
    ("APAC",          "Australia",     "New South Wales",   "Sydney"),
    ("APAC",          "Singapore",     "Singapore",         "Singapore"),
    ("LATAM",         "Mexico",        "Mexico City",       "Mexico City"),
    ("LATAM",         "Mexico",        "Jalisco",           "Guadalajara"),
    ("LATAM",         "Brazil",        "São Paulo",         "São Paulo"),
    ("LATAM",         "Brazil",        "Rio de Janeiro",    "Rio de Janeiro"),
]
FORMATS        = ["Hypermarket", "Supermarket", "Convenience", "Express"]
FORMAT_WEIGHTS = [0.15, 0.40, 0.30, 0.15]

stores = []
for i, (region, country, state, city) in enumerate(STORE_LOCATIONS, start=1):
    stores.append({
        "StoreID":      f"STR-{i:03d}",
        "StoreName":    f"Store_{i:03d}",
        "Region":       region,
        "Market":       country,
        "Country":      country,
        "State":        state,
        "City":         city,
        "StoreFormat":  str(RNG.choice(FORMATS, p=FORMAT_WEIGHTS)),
        "StoreSizeSqM": int(RNG.integers(200, 12000)),
        "OpenDate":     date(int(RNG.integers(2010, 2023)), int(RNG.integers(1, 13)), 1),
        "StoreStatus":  "Remodeling" if RNG.random() < 0.05 else "Active",
    })

df_stores = pd.DataFrame(stores)
eng = make_engine()
with eng.begin() as conn:
    conn.execute(text("DELETE FROM dbo.dim_store"))
df_stores.to_sql("dim_store", eng, schema="dbo", if_exists="append", index=False)
print(f"dim_store: {len(df_stores)} filas cargadas ✓")
print(df_stores[["StoreID","Region","Country","City","StoreFormat"]].to_string(index=False))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 3 — `dim_product` (100 SKUs, inglés)
# 7 categorías con sesgo intencional para el análisis de varianza (Stationery +15%, Electronics −12%). Precios en USD.

# CELL ********************

N_PRODUCTS = 100
CATALOG = {
    "Beverages":     {"code":"BEV","share":0.20,"subcats":["Soft Drinks","Water","Juices","Dairy","Energy Drinks"],"price_range":(1,8),  "cost_factor":0.55},
    "Food":          {"code":"FOO","share":0.25,"subcats":["Snacks","Cereal","Canned Goods","Pasta","Condiments"], "price_range":(1,12), "cost_factor":0.60},
    "Cleaning":      {"code":"CLN","share":0.15,"subcats":["Detergents","Disinfectants","Paper Goods","Air Fresheners"],"price_range":(2,15),"cost_factor":0.50},
    "Personal Care": {"code":"PCR","share":0.15,"subcats":["Shampoo","Lotions","Deodorants","Oral Care"],          "price_range":(2,20), "cost_factor":0.52},
    "Stationery":    {"code":"STA","share":0.10,"subcats":["Notebooks","School Supplies","Office"],                "price_range":(1,25), "cost_factor":0.45},
    "Apparel":       {"code":"APP","share":0.10,"subcats":["Casual Wear","Sportswear","Footwear"],                 "price_range":(8,80), "cost_factor":0.40},
    "Electronics":   {"code":"ELE","share":0.05,"subcats":["Accessories","Chargers","Headphones"],                 "price_range":(5,60), "cost_factor":0.58},
}

products, sku_id = [], 1
for cat, meta in CATALOG.items():
    pmin, pmax = meta["price_range"]
    for _ in range(round(N_PRODUCTS * meta["share"])):
        subcat = meta["subcats"][RNG.integers(0, len(meta["subcats"]))]
        price  = round(float(RNG.uniform(pmin, pmax)), 2)
        cost   = round(price * meta["cost_factor"] * float(RNG.uniform(0.85, 1.15)), 2)
        products.append({
            "SKU":             f"SKU-{sku_id:04d}",
            "ProductName":     f"Product_{sku_id:04d}",
            "Category":        cat,
            "CategoryCode":    meta["code"],
            "Subcategory":     subcat,
            "SubcategoryCode": f"{meta['code'][:2]}{meta['subcats'].index(subcat)+1:02d}",
            "Brand":           f"Brand_{int(RNG.integers(1, 51)):02d}",
            "UnitListPrice":   price,
            "UnitCost":        cost,
            "PackSize":        str(RNG.choice(["1-pack","6-pack","12-pack","Single"])),
            "UnitOfMeasure":   "EA",
            "LaunchDate":      date(int(RNG.integers(2019, 2026)), int(RNG.integers(1, 13)), 1),
            "IsSeasonal":      int(RNG.random() < 0.08),
            "LifecycleStatus": str(RNG.choice(["Active","Phase-Out","Discontinued"], p=[0.92, 0.05, 0.03])),
        })
        sku_id += 1

while len(products) < N_PRODUCTS:
    clone = products[-1].copy()
    clone["SKU"], clone["ProductName"] = f"SKU-{sku_id:04d}", f"Product_{sku_id:04d}"
    products.append(clone); sku_id += 1

df_products = pd.DataFrame(products[:N_PRODUCTS])
eng = make_engine()
with eng.begin() as conn:
    conn.execute(text("DELETE FROM dbo.dim_product"))
df_products.to_sql("dim_product", eng, schema="dbo", if_exists="append", index=False)
print(f"dim_product: {len(df_products)} filas cargadas ✓")
print(df_products["Category"].value_counts().to_string())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 4 — Leer llaves de regreso
# Normaliza fechas a `Timestamp` y filtra al rango de ventas (últimos 6 meses).

# CELL ********************

eng = make_engine()
df_store_keys   = pd.read_sql("SELECT StoreKey, StoreID, Region, StoreFormat FROM dbo.dim_store", eng)
df_product_keys = pd.read_sql(
    "SELECT ProductKey, SKU, Category, UnitListPrice, IsSeasonal, LifecycleStatus, LaunchDate "
    "FROM dbo.dim_product", eng)
df_date_keys_all = pd.read_sql("SELECT DateKey, [Date], IsHoliday, RetailSeason FROM dbo.dim_date", eng)

df_date_keys_all["Date"]      = pd.to_datetime(df_date_keys_all["Date"])
df_product_keys["LaunchDate"] = pd.to_datetime(df_product_keys["LaunchDate"])

# Ventana histórica: usada por actuals y por el forecast del pasado (para MAPE)
df_date_keys = df_date_keys_all[
    (df_date_keys_all["Date"] >= pd.Timestamp(DATE_START)) &
    (df_date_keys_all["Date"] <= pd.Timestamp(DATE_END))
].sort_values("DateKey").reset_index(drop=True)

# Ventana futura: solo forecast, sin actuals (planning horizon)
df_date_keys_future = df_date_keys_all[
    (df_date_keys_all["Date"] >  pd.Timestamp(DATE_END)) &
    (df_date_keys_all["Date"] <= pd.Timestamp(FUTURE_END))
].sort_values("DateKey").reset_index(drop=True)

assert len(df_date_keys) > 0,        "df_date_keys vacío — ¿corriste dim_date?"
assert len(df_date_keys_future) > 0, "df_date_keys_future vacío — revisa FUTURE_END vs dim_date end"
print(f"Stores: {len(df_store_keys)}  |  Products: {len(df_product_keys)}")
print(f"History days: {len(df_date_keys)}  ({df_date_keys['Date'].min().date()} → {df_date_keys['Date'].max().date()})")
print(f"Future days:  {len(df_date_keys_future)}  ({df_date_keys_future['Date'].min().date()} → {df_date_keys_future['Date'].max().date()})")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 5 — `fact_actual_sales` (pandas, vectorizado)
# Genera la demanda con numpy por par tienda×SKU y escribe con `to_sql`. **Sin Spark.** A este tamaño cabe entero en memoria.

# CELL ********************

FORMAT_COVERAGE = {"Hypermarket": 0.85, "Supermarket": 0.70, "Convenience": 0.40, "Express": 0.50}
SEASON_MULT  = {"Back-to-School": 1.25, "Black Friday": 1.80, "Holiday": 1.50, "Regular": 1.00}
WEEKDAY_MULT = {1: 0.85, 2: 0.85, 3: 0.90, 4: 0.95, 5: 1.10, 6: 1.25, 7: 1.10}

# Qué SKUs vende cada tienda (según formato)
all_pks = df_product_keys["ProductKey"].to_numpy()
from collections import defaultdict
store_to_skus = defaultdict(list)
for _, s in df_store_keys.iterrows():
    cov = FORMAT_COVERAGE.get(s["StoreFormat"], 0.60)
    store_to_skus[int(s["StoreKey"])] = RNG.choice(
        all_pks, size=int(len(all_pks)*cov), replace=False).tolist()
print(f"Pares tienda×SKU activos: {sum(len(v) for v in store_to_skus.values()):,}")

# Multiplicadores por día (vectorizados)
n_days       = len(df_date_keys)
dk_arr       = df_date_keys["DateKey"].to_numpy()
date_arr     = df_date_keys["Date"].to_numpy()
season_arr   = df_date_keys["RetailSeason"].to_numpy()
weekday_arr  = (df_date_keys["Date"].dt.dayofweek + 1).to_numpy()
holiday_arr  = df_date_keys["IsHoliday"].to_numpy().astype(float)

season_mult   = np.array([SEASON_MULT.get(s, 1.0) for s in season_arr])
weekday_mult  = np.array([WEEKDAY_MULT.get(int(w), 1.0) for w in weekday_arr])
holiday_mult  = np.where(holiday_arr > 0, 1.20, 1.0)
base_day_mult = season_mult * weekday_mult * holiday_mult
seasonal_boost = np.where(np.isin(season_arr, ["Back-to-School","Holiday","Black Friday"]), 1.40, 1.0)

price_by_pk    = df_product_keys.set_index("ProductKey")["UnitListPrice"].to_dict()
launch_by_pk   = df_product_keys.set_index("ProductKey")["LaunchDate"].to_dict()
seasonal_by_pk = df_product_keys.set_index("ProductKey")["IsSeasonal"].to_dict()

def build_store_block(sk):
    parts = []
    for pk in store_to_skus[sk]:
        launch   = np.datetime64(launch_by_pk[pk])
        price    = float(price_by_pk[pk])
        mult     = base_day_mult * (seasonal_boost if seasonal_by_pk[pk] else 1.0)
        base_dem = float(RNG.integers(2, 30))
        qty      = RNG.negative_binomial(5, 5.0 / (5.0 + base_dem * mult)).astype(float)
        keep = (qty > 0) & (date_arr >= launch) & (RNG.random(n_days) >= 0.12)
        m = int(keep.sum())
        if m == 0:
            continue
        q     = qty[keep]
        gross = np.round(q * price, 2)
        promo = RNG.random(m) < 0.08
        disc  = np.round(np.where(promo, gross * RNG.uniform(0.05, 0.25, m), 0.0), 2)
        txn   = RNG.integers(1, np.maximum(2, q.astype(int) + 1))
        promoid = np.full(m, None, dtype=object)
        npr = int(promo.sum())
        if npr:
            promoid[promo] = [f"PROMO-{int(x):02d}" for x in RNG.integers(1, 50, npr)]
        parts.append(pd.DataFrame({
            "DateKey": dk_arr[keep], "StoreKey": sk, "ProductKey": pk,
            "ActualQuantity": q, "GrossRevenue": gross, "DiscountAmount": disc,
            "TransactionCount": txn, "PromotionFlag": promo.astype(int), "PromotionID": promoid,
        }))
    return pd.concat(parts, ignore_index=True) if parts else None

# Genera TODO en memoria (dataset pequeño)
blocks = [b for b in (build_store_block(sk) for sk in store_to_skus) if b is not None]
df_actuals = pd.concat(blocks, ignore_index=True)
df_actuals["PromotionID"] = df_actuals["PromotionID"].astype(object).where(df_actuals["PromotionID"].notna(), None)
print(f"Generadas {len(df_actuals):,} filas de actuals")

# Escribe con pandas
eng = make_engine()
with eng.begin() as conn:
    conn.execute(text("DELETE FROM dbo.fact_actual_sales"))
df_actuals.to_sql("fact_actual_sales", eng, schema="dbo",
                  if_exists="append", index=False, chunksize=10_000)
print(f"fact_actual_sales: {len(df_actuals):,} filas cargadas ✓")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 6 — `fact_forecast` (pandas, derivado de actuals)
# **v1 Statistical**: media móvil 7d × sesgo por categoría. **v2 Manual Override**: reglas del planner sobre v1. Todo en pandas reutilizando `df_actuals` en memoria.

# CELL ********************

CATEGORY_BIAS = {
    "Beverages": 0.08, "Food": 0.03, "Cleaning": -0.05, "Personal Care": 0.06,
    "Stationery": 0.15, "Apparel": -0.08, "Electronics": -0.12,
}

# Multiplicadores (mismos que Celda 5, para extender al futuro de forma consistente)
SEASON_MULT  = {"Back-to-School": 1.25, "Black Friday": 1.80, "Holiday": 1.50, "Regular": 1.00}
WEEKDAY_MULT = {1: 0.85, 2: 0.85, 3: 0.90, 4: 0.95, 5: 1.10, 6: 1.25, 7: 1.10}

# Trae Category, UnitListPrice y RetailSeason a las filas de actuals (pasado)
df = (df_actuals
    .merge(df_product_keys[["ProductKey","Category","UnitListPrice"]], on="ProductKey", how="left")
    .merge(df_date_keys[["DateKey","RetailSeason"]], on="DateKey", how="left")
    .sort_values(["StoreKey","ProductKey","DateKey"])
    .reset_index(drop=True))

# Media móvil de 7 días (excluye el día actual con shift(1))
df["RollingAvgQty"] = (df.groupby(["StoreKey","ProductKey"])["ActualQuantity"]
                         .transform(lambda s: s.shift(1).rolling(7, min_periods=1).mean()))
df["RollingAvgQty"] = df["RollingAvgQty"].fillna(0)

CREATION_DATE_KEY = int(df_date_keys["DateKey"].iloc[0])
df["CategoryBias"] = df["Category"].map(CATEGORY_BIAS).fillna(0.0)

base_qty = np.where(df["RollingAvgQty"] > 0, df["RollingAvgQty"], df["ActualQuantity"])

# ── v1 Statistical — PASADO (sobre actuals, para MAPE) ────────────────────────
v1_past = pd.DataFrame({
    "ForecastVersion":   "Statistical",
    "ForecastVersionID": 1,
    "CreationDateKey":   CREATION_DATE_KEY,
    "ForecastDateKey":   df["DateKey"],
    "StoreKey":          df["StoreKey"],
    "ProductKey":        df["ProductKey"],
    "ForecastQuantity":  np.round(base_qty * (1 + df["CategoryBias"]), 2),
})
v1_past["ForecastRevenue"] = np.round(v1_past["ForecastQuantity"] * df["UnitListPrice"], 2)
v1_past["LowerBound"]      = np.round(v1_past["ForecastQuantity"] * 0.85, 2)
v1_past["UpperBound"]      = np.round(v1_past["ForecastQuantity"] * 1.15, 2)
v1_past["ForecastModel"]   = "MovingAvg7D"
v1_past["CreatedBy"]       = "system"

# ── v1 Statistical — FUTURO (extiende el horizonte 6 meses adelante) ──────────
# Baseline por (Store, Product) = media de los últimos 7 días reales; fallback a media total
last7 = (df.sort_values(["StoreKey","ProductKey","DateKey"])
           .groupby(["StoreKey","ProductKey"])["ActualQuantity"]
           .apply(lambda s: s.tail(7).mean())
           .reset_index(name="BaseQty"))
last7["BaseQty"] = last7["BaseQty"].fillna(last7["BaseQty"].mean())

# Cross-join pares activos × días futuros
future_skeleton = last7.merge(df_date_keys_future, how="cross")
future_skeleton = future_skeleton.merge(
    df_product_keys[["ProductKey","Category","UnitListPrice"]], on="ProductKey", how="left")

# Multiplicadores vectorizados para el futuro
season_mult_f  = future_skeleton["RetailSeason"].map(SEASON_MULT).fillna(1.0).to_numpy()
weekday_mult_f = (future_skeleton["Date"].dt.dayofweek + 1).map(WEEKDAY_MULT).fillna(1.0).to_numpy()
holiday_mult_f = np.where(future_skeleton["IsHoliday"].to_numpy() > 0, 1.20, 1.0)
cat_bias_f     = future_skeleton["Category"].map(CATEGORY_BIAS).fillna(0.0).to_numpy()

fcst_qty_f = np.round(
    future_skeleton["BaseQty"].to_numpy()
    * season_mult_f * weekday_mult_f * holiday_mult_f
    * (1 + cat_bias_f),
    2)

v1_future = pd.DataFrame({
    "ForecastVersion":   "Statistical",
    "ForecastVersionID": 1,
    "CreationDateKey":   CREATION_DATE_KEY,
    "ForecastDateKey":   future_skeleton["DateKey"].to_numpy(),
    "StoreKey":          future_skeleton["StoreKey"].to_numpy(),
    "ProductKey":        future_skeleton["ProductKey"].to_numpy(),
    "ForecastQuantity":  fcst_qty_f,
    "ForecastRevenue":   np.round(fcst_qty_f * future_skeleton["UnitListPrice"].to_numpy(), 2),
    "LowerBound":        np.round(fcst_qty_f * 0.85, 2),
    "UpperBound":        np.round(fcst_qty_f * 1.15, 2),
    "ForecastModel":     "MovingAvg7D",
    "CreatedBy":         "system",
})

# v1 = pasado + futuro
v1 = pd.concat([v1_past, v1_future], ignore_index=True)
print(f"v1 Statistical: {len(v1_past):,} pasado + {len(v1_future):,} futuro = {len(v1):,} filas")

# ── v2 Manual Override ─────────────────────────────────────────────────────────
# Para que el override funcione en pasado Y futuro, anexamos Category y RetailSeason
# directamente a v1 (no a `df`, que solo tiene el pasado).
v1 = (v1
    .merge(df_product_keys[["ProductKey","Category"]], on="ProductKey", how="left")
    .merge(df_date_keys_all[["DateKey","RetailSeason"]]
             .rename(columns={"DateKey":"ForecastDateKey"}),
           on="ForecastDateKey", how="left"))

override = np.select(
    [
        (v1["Category"] == "Stationery")  & (v1["RetailSeason"] == "Back-to-School"),
        (v1["Category"] == "Electronics") & (v1["RetailSeason"] == "Black Friday"),
        (v1["Category"] == "Beverages")   & (v1["RetailSeason"] == "Holiday"),
    ],
    [1.25, 1.30, 1.15], default=1.0)

v2 = v1.copy()
v2["ForecastVersion"]   = "Manual Override"
v2["ForecastVersionID"] = 2
v2["ForecastQuantity"]  = np.round(v1["ForecastQuantity"] * override, 2)
v2["ForecastRevenue"]   = np.round(v1["ForecastRevenue"]  * override, 2)
v2["LowerBound"]        = np.round(v1["LowerBound"]        * override, 2)
v2["UpperBound"]        = np.round(v1["UpperBound"]        * override, 2)
v2["ForecastModel"]     = "Manual"
v2["CreatedBy"]         = "planner_01"

cols = ["ForecastVersion","ForecastVersionID","CreationDateKey","ForecastDateKey",
        "StoreKey","ProductKey","ForecastQuantity","ForecastRevenue",
        "LowerBound","UpperBound","ForecastModel","CreatedBy"]
df_forecast = pd.concat([v1[cols], v2[cols]], ignore_index=True)
print(f"Generadas {len(df_forecast):,} filas de forecast (v1 + v2)")

eng = make_engine()
with eng.begin() as conn:
    conn.execute(text("DELETE FROM dbo.fact_forecast"))
df_forecast.to_sql("fact_forecast", eng, schema="dbo",
                   if_exists="append", index=False, chunksize=10_000)
print(f"fact_forecast: {len(df_forecast):,} filas cargadas ✓")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 7 — `fact_planning_scenario` (pandas)
# Tres escenarios de demostración en inglés.

# CELL ********************

SCENARIOS = [
    {"name": "Back-to-School Stationery +25%", "description": "Seasonal uplift in school supplies",
     "category": "Stationery",  "season": "Back-to-School", "adj_pct": 0.25},
    {"name": "Black Friday Electronics +30%",  "description": "Promotional uplift for Black Friday",
     "category": "Electronics", "season": "Black Friday",   "adj_pct": 0.30},
    {"name": "Supply Constraint Beverages -15%","description": "Reduction due to inventory constraint",
     "category": "Beverages",   "season": "Regular",        "adj_pct": -0.15},
    # ── Nuevos para el demo ──
    {"name": "Best-Case Demand +25%",  "description": "Strong economic conditions, higher demand",
     "category": None, "season": None, "adj_pct": 0.25},
    {"name": "Worst-Case Demand -20%", "description": "Recession / competitor action / weak demand",
     "category": None, "season": None, "adj_pct": -0.20},
]

eng = make_engine()
df_fc = pd.read_sql(
    "SELECT ForecastDateKey, StoreKey, ProductKey, ForecastQuantity "
    "FROM dbo.fact_forecast WHERE ForecastVersionID = 1", eng)
df_fc = (df_fc
    .merge(df_product_keys[["ProductKey","Category"]], on="ProductKey", how="left")
    .merge(df_date_keys[["DateKey","RetailSeason"]].rename(columns={"DateKey":"ForecastDateKey"}),
           on="ForecastDateKey", how="left"))

rows = []
for sc in SCENARIOS:
    if sc["category"] is None:        # escenario global (best/worst case → todo el catálogo)
        sub = df_fc.copy()
    else:                              # escenario por categoría + temporada
        sub = df_fc[(df_fc["Category"]==sc["category"]) & (df_fc["RetailSeason"]==sc["season"])].copy()
    if sub.empty:
        print(f"  ⚠ Sin filas para: {sc['name']}"); continue
    sub = sub.sample(min(20000, len(sub)), random_state=SEED)
    sub["ScenarioName"]          = sc["name"]
    sub["ScenarioDescription"]   = sc["description"]
    sub["BaseForecastVersionID"] = 1
    sub["DateKey"]               = sub["ForecastDateKey"]
    sub["AdjustmentType"]        = "Percent"
    sub["AdjustmentPct"]         = sc["adj_pct"]
    sub["AdjustmentAbsolute"]    = None
    sub["BaselineForecast"]      = sub["ForecastQuantity"]
    sub["AdjustedForecast"]      = (sub["ForecastQuantity"] * (1 + sc["adj_pct"])).round(2)
    sub["CreatedBy"]             = "planner_01"
    sub["IsActive"]              = 1
    rows.append(sub[["ScenarioName","ScenarioDescription","BaseForecastVersionID","DateKey",
                     "StoreKey","ProductKey","AdjustmentType","AdjustmentPct","AdjustmentAbsolute",
                     "BaselineForecast","AdjustedForecast","CreatedBy","IsActive"]])
    print(f"  '{sc['name']}': {len(sub):,} filas")

df_scen = pd.concat(rows, ignore_index=True)

# Red de seguridad: elimina duplicados en el grain antes de insertar
df_scen = df_scen.drop_duplicates(
    subset=["ScenarioName", "DateKey", "StoreKey", "ProductKey"]
).reset_index(drop=True)

eng = make_engine()
with eng.begin() as conn:
    conn.execute(text("DELETE FROM dbo.fact_planning_scenario"))
df_scen.to_sql("fact_planning_scenario", eng, schema="dbo",
               if_exists="append", index=False, chunksize=5000)
print(f"\nfact_planning_scenario: {len(df_scen):,} filas cargadas ✓")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Celda 8 — Verificación + MAPE por categoría
# Stationery y Electronics deberían tener el MAPE más alto (sesgo intencional).

# CELL ********************

eng = make_engine()
conteos = pd.read_sql("""
SELECT 'dim_date' AS tabla, COUNT(*) AS filas FROM dbo.dim_date
UNION ALL SELECT 'dim_store',              COUNT(*) FROM dbo.dim_store
UNION ALL SELECT 'dim_product',            COUNT(*) FROM dbo.dim_product
UNION ALL SELECT 'fact_actual_sales',      COUNT(*) FROM dbo.fact_actual_sales
UNION ALL SELECT 'fact_forecast',          COUNT(*) FROM dbo.fact_forecast
UNION ALL SELECT 'fact_planning_scenario', COUNT(*) FROM dbo.fact_planning_scenario
""", eng)
print(conteos.to_string(index=False))

mape = pd.read_sql("""
SELECT  p.Category,
        COUNT(*) AS records,
        ROUND(AVG(a.ActualQuantity), 2)   AS qty_actual_avg,
        ROUND(AVG(f.ForecastQuantity), 2) AS qty_fcst_avg,
        ROUND(AVG(ABS(a.ActualQuantity - f.ForecastQuantity)
              / NULLIF(f.ForecastQuantity, 0)) * 100, 1) AS mape_pct
FROM  dbo.fact_actual_sales a
JOIN  dbo.fact_forecast     f ON a.DateKey=f.ForecastDateKey AND a.StoreKey=f.StoreKey
                             AND a.ProductKey=f.ProductKey AND f.ForecastVersionID=1
JOIN  dbo.dim_product       p ON p.ProductKey=a.ProductKey
GROUP BY p.Category
ORDER BY mape_pct DESC
""", eng)
print("\nMAPE by category (v1 Statistical vs Actual):")
print(mape.to_string(index=False))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
