# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "3f259435-66c7-4513-8c73-17fd9965a872",
# META       "default_lakehouse_name": "Loan_Data",
# META       "default_lakehouse_workspace_id": "1beb3139-2c5d-4cb3-b416-c46404555b49",
# META       "known_lakehouses": [
# META         {
# META           "id": "3f259435-66c7-4513-8c73-17fd9965a872"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Fraud Detection Model

# MARKDOWN ********************

# ## Extract

# CELL ********************

# Use pip to install imblearn
%pip install imblearn

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Set the variables needed to locate the dataset, indicate the target column name and the experiment name

# CELL ********************

IS_CUSTOM_DATA = False  # If True, the dataset has to be uploaded manually

TARGET_COL = "Class"  # Target column name
IS_SAMPLE = False  # If True, use only <SAMPLE_ROWS> rows of data for training; otherwise, use all data
SAMPLE_ROWS = 5000  # If IS_SAMPLE is True, use only this number of rows for training

DATA_FOLDER = "Files/fraud-detection/"  # Folder with data files
DATA_FILE = "creditcard.csv"  # Data file name

EXPERIMENT_NAME = "aisample-fraud"  # MLflow experiment name

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### This cell will download a publicly available dataset into the attached lakehouse. The program will ignore this operation if the dataset already exists in the attached lakehouse.

# CELL ********************

if not IS_CUSTOM_DATA:
    # Download data files into the lakehouse if they're not already there
    import os, requests

    remote_url = "https://synapseaisolutionsa.z13.web.core.windows.net/data/Credit_Card_Fraud_Detection"
    fname = "creditcard.csv"
    download_path = f"/lakehouse/default/{DATA_FOLDER}/raw"

    if not os.path.exists("/lakehouse/default"):
        raise FileNotFoundError("Default lakehouse not found, please add a lakehouse and restart the session.")
    os.makedirs(download_path, exist_ok=True)
    if not os.path.exists(f"{download_path}/{fname}"):
        r = requests.get(f"{remote_url}/{fname}", timeout=30)
        with open(f"{download_path}/{fname}", "wb") as f:
            f.write(r.content)
    print("Downloaded demo data files into lakehouse.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Set up MLfLow

# CELL ********************

# Set up MLflow for experiment tracking
import mlflow

mlflow.set_experiment(EXPERIMENT_NAME)
mlflow.autolog(disable=True)  # Disable MLflow autologging

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", True)
    .load(f"{DATA_FOLDER}/raw/{DATA_FILE}")
    .cache()
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Synthetic modification

# CELL ********************

IS_CUSTOM_DATA = False  # If True, the dataset has to be uploaded manually

TARGET_COL = "Class"  # Target column name
IS_SAMPLE = False  # If True, use only <SAMPLE_ROWS> rows of data for training; otherwise, use all data
SAMPLE_ROWS = 5000  # If IS_SAMPLE is True, use only this number of rows for training

DATA_FOLDER = "Files/fraud-detection/"  # Folder with data files
DATA_FILE = "creditcard.csv"  # Data file name

EXPERIMENT_NAME = "aisample-fraud"  # MLflow experiment name

df = (
    spark.read.format("csv")
    .option("header", "true")
    .option("inferSchema", True)
    .load(f"{DATA_FOLDER}/raw/{DATA_FILE}")
    .cache()
)

from pyspark.sql import functions as F
begin_day = "2026-07-21 00:00:00"

df = df.withColumn(
    "date_time",
    F.from_unixtime(F.unix_timestamp(F.lit(begin_day)) + F.col("Time")).cast("timestamp")
)

df = df.withColumn("Date", F.to_date("date_time"))

df = df.drop("date_time")

df = df.withColumnsRenamed(
    {
        "V1": "CustomerRiskScore",
        "V2": "TransactionVelocity",
        "V3": "MerchantTrustScore",
        "V4": "SpendingPatternIndex",
        "V5": "GeographicRisk",
        "V6": "DeviceRiskScore",
        "V7": "MerchantCategoryRisk",
        "V8": "CardUsageFrequency",
        "V9": "TransactionAnomalyScore",
        "V10": "BehavioralDeviation",
        "V11": "CustomerLoyaltyIndex",
        "V12": "FraudPatternScore",
        "V13": "AccountStability",
        "V14": "IdentityConfidence",
        "V15": "CustomerTenureScore",
        "V16": "HistoricalFraudRisk",
        "V17": "CardSecurityScore",
        "V18": "MerchantReputation",
        "V19": "TransactionConsistency",
        "V20": "SessionRiskScore",
        "V21": "PurchaseFrequency",
        "V22": "AverageSpendingIndex",
        "V23": "CrossBorderIndicator",
        "V24": "TimePatternScore",
        "V25": "LocationConsistency",
        "V26": "PaymentBehaviorScore",
        "V27": "DigitalActivityScore",
        "V28": "OverallRiskIndicator"
    }
)

all_cols = df.columns
all_cols.remove("Date")

df = df.select("Date", *all_cols)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = df.withColumns({
    "TransactionChannel":
        F.when(F.rand() < 0.55, "mobile_app")
        .when(F.rand() < 0.69, "atm")
        .when(F.rand() < 0.75, "online_banking")
        .when(F.rand() < 0.8, "api")
        .when(F.rand() < 0.88, "ecommerce")
        .when(F.rand() < 0.95, "in_person")
        .otherwise("pos"),
    "TransactionCountry":
        F.when(F.rand() < 0.50, "India")
        .when(F.rand() < 0.52, "Brazil")
        .when(F.rand() < 0.55, "Mexico")
        .when(F.rand() < 0.60, "UnitedStates")
        .when(F.rand() < 0.75, "Canada")
        .when(F.rand() < 0.78, "Spain")
        .when(F.rand() < 0.83, "Germany")
        .otherwise("Japan")
})

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
begin_day = "2026-07-21 00:00:00"

df = df.withColumn(
    "Date_Time",
    F.from_unixtime(F.unix_timestamp(F.lit(begin_day)) + F.col("Time")).cast("timestamp")
)
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.ml.feature import Bucketizer

splits = (df.select("Amount").approxQuantile("Amount", [i/10 for i in range(11)], 0.01))

bucketizer = Bucketizer(
    splits=splits,
    inputCol="Amount",
    outputCol="Amount_Bin"
)

df = bucketizer.transform(df)
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import IntegerType
df = df.withColumn('Amount_Bin', F.col("Amount_Bin").cast(IntegerType()))

from pyspark.sql import functions as F
df = df.withColumn(
    "Date_Time_Truncate",
    F.date_trunc("hour", F.col("Date_Time"))
)

df = df.drop("Date_Time")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Exploratory Data Analysis

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Print dataset basic information
print("records read: " + str(df.count()))
print("Schema: ")
df.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Cast the target column into the correct type. The documentation decided that the target column must be last column of the dataset.

# CELL ********************

import pyspark.sql.functions as F

df_columns = df.columns
df_columns.remove(TARGET_COL)

# Ensure that TARGET_COL is the last column
df = df.select(df_columns + [TARGET_COL]).withColumn(TARGET_COL, F.col(TARGET_COL).cast("int"))

if IS_SAMPLE:
    df = df.limit(SAMPLE_ROWS)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### The spark dataframe is transformed into a pandas dataframe for easier data manipulation and greater compatibility with other models.

# CELL ********************

df_pd = df.toPandas()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Quantitative data distribution

# CELL ********************

# The distribution of classes in the dataset
print('No Frauds', round(df_pd['Class'].value_counts()[0]/len(df_pd) * 100,2), '% of the dataset')
print('Frauds', round(df_pd['Class'].value_counts()[1]/len(df_pd) * 100,2), '% of the dataset')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Visual data distribution

# CELL ********************

import seaborn as sns
import matplotlib.pyplot as plt

colors = ["#0101DF", "#DF0101"]
sns.countplot(x='Class', data=df_pd, palette=colors) 
plt.title('Class Distributions \n (0: No Fraud || 1: Fraud)', fontsize=10)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Boxplots: the left boxplot displays the outliers, the right boxplot displays the minimum, first quartile, median, third quartile and maximum.

# CELL ********************

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12,5))
s = sns.boxplot(ax = ax1, x="Class", y="Amount", hue="Class",data=df_pd, palette="PRGn", showfliers=True) # Remove outliers from the plot
s = sns.boxplot(ax = ax2, x="Class", y="Amount", hue="Class",data=df_pd, palette="PRGn", showfliers=False) # Keep outliers from the plot
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Transform

# MARKDOWN ********************

# ##### Split the data into training and testing sets

# CELL ********************

from sklearn.model_selection import train_test_split

train, test = train_test_split(df_pd, test_size=0.15)
feature_cols = [c for c in df_pd.columns.tolist() if c not in [TARGET_COL]]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Due to the data is imbalanced, SMOTE will be applied only to the training dataset in order to avoid data leakage

# CELL ********************

# Apply SMOTE to the training data
import pandas as pd
from collections import Counter
from imblearn.over_sampling import SMOTE

X = train[feature_cols]
y = train[TARGET_COL]
print("Original dataset shape %s" % Counter(y))

sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)
print("Resampled dataset shape %s" % Counter(y_res))

new_train = pd.concat([X_res, y_res], axis=1)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Set (exclusive = False) in order to track more metrics, parameters and files

# CELL ********************

mlflow.autolog(exclusive=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Train 2 different models, both with LightGBM. One for the imbalanced dataset, and other for balanced dataset.

# CELL ********************

import lightgbm as lgb

model = lgb.LGBMClassifier(objective="binary") # Imbalanced dataset
smote_model = lgb.LGBMClassifier(objective="binary") # Balanced dataset

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Train LightGBM for both imbalanced and balanced datasets and define the evaluation metrics
print("Start training with imbalanced data:\n")
with mlflow.start_run(run_name="raw_data") as raw_run:
    model = model.fit(
        train[feature_cols],
        train[TARGET_COL],
        eval_set=[(test[feature_cols], test[TARGET_COL])],
        eval_metric="auc",
        callbacks=[
            lgb.log_evaluation(10),
        ],
    )

print(f"\n\nStart training with balanced data:\n")
with mlflow.start_run(run_name="smote_data") as smote_run:
    smote_model = smote_model.fit(
        new_train[feature_cols],
        new_train[TARGET_COL],
        eval_set=[(test[feature_cols], test[TARGET_COL])],
        eval_metric="auc",
        callbacks=[
            lgb.log_evaluation(10),
        ],
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Determine feature importance for both trained models. The important features show significant differences when comparing a model with imbalance dataset with a balanced dataset.

# CELL ********************

# Feature importance in imabalanced data
with mlflow.start_run(run_id=raw_run.info.run_id):
    importance = lgb.plot_importance(
        model, title="Feature importance for imbalanced data"
    )
    importance.figure.savefig("feauture_importance.png")
    mlflow.log_figure(importance.figure, "feature_importance.png")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Feature importance in balanced data
with mlflow.start_run(run_id=smote_run.info.run_id):
    smote_importance = lgb.plot_importance(
        smote_model, title="Feature importance for balanced (via SMOTE) data"
    )
    smote_importance.figure.savefig("feauture_importance_smote.png")
    mlflow.log_figure(smote_importance.figure, "feauture_importance_smote.png")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Evaluation

# MARKDOWN ********************

# ##### Function that makes predictions and converts the prediction result into a spark dataframe

# CELL ********************

from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, DoubleType

def prediction_to_spark(model, test):
    predictions = model.predict(test[feature_cols], num_iteration=model.best_iteration_)
    predictions = tuple(zip(test[TARGET_COL].tolist(), predictions.tolist()))
    dataColumns = [TARGET_COL, "prediction"]
    predictions = (
        spark.createDataFrame(data=predictions, schema=dataColumns)
        .withColumn(TARGET_COL, col(TARGET_COL).cast(IntegerType()))
        .withColumn("prediction", col("prediction").cast(DoubleType()))
    )

    return predictions

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Make predictions for both models

# CELL ********************

predictions = prediction_to_spark(model, test)
smote_predictions = prediction_to_spark(smote_model, test)
predictions.limit(10).toPandas()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Compute metrics for the two models

# CELL ********************

from synapse.ml.train import ComputeModelStatistics

metrics = ComputeModelStatistics(
    evaluationMetric="classification", labelCol=TARGET_COL, scoredLabelsCol="prediction"
).transform(predictions)

smote_metrics = ComputeModelStatistics(
    evaluationMetric="classification", labelCol=TARGET_COL, scoredLabelsCol="prediction"
).transform(smote_predictions)
print('Imbalanced Model:')
display(metrics)

print('Balanced Model:')
display(smote_metrics)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Build confusion matrix

# CELL ********************

# Collect confusion matrix values
cm = metrics.select("confusion_matrix").collect()[0][0].toArray()
smote_cm = smote_metrics.select("confusion_matrix").collect()[0][0].toArray()
print(cm)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Personalized color map
light_blue = LinearSegmentedColormap.from_list(
    "light_blue",
    ["#c5d6ed", "#6490cf"]
)

# Plot the confusion matrix
def plot(cm):
    """
    Plot the confusion matrix.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.heatmap(cm, annot=False, cmap=light_blue, ax=ax)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j + 0.5,
                i + 0.5,
                str(int(cm[i, j])),
                ha="center",
                va="center",
                color="black",
                fontsize=12
            )
    ax.set_title("Confusion Matrix")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    return ax

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Plot the confusion matrix for the predictions of the balanced model

# CELL ********************

with mlflow.start_run(run_id=smote_run.info.run_id):
    ax = plot(smote_cm)
    mlflow.log_figure(ax.figure, "ConfusionMatrix.png")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Plot the confusion matrix for the predictions of the imbalanced model

# CELL ********************

with mlflow.start_run(run_id=raw_run.info.run_id):
    ax = plot(cm)
    mlflow.log_figure(ax.figure, "ConfusionMatrix.png")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Function that evaluates a model with AUC-ROC and AUPRC measures

# CELL ********************

from pyspark.ml.evaluation import BinaryClassificationEvaluator

def evaluate(predictions):
    """
    Evaluate the model by computing AUROC and AUPRC with the predictions.
    """

    # Initialize the binary evaluator
    evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction", labelCol=TARGET_COL)

    _evaluator = lambda metric: evaluator.setMetricName(metric).evaluate(predictions)

    # Calculate AUROC, baseline 0.5
    auroc = _evaluator("areaUnderROC")
    print(f"The AUROC is: {auroc:.4f}")

    # Calculate AUPRC, baseline positive rate (0.172% in the data)
    auprc = _evaluator("areaUnderPR")
    print(f"The AUPRC is: {auprc:.4f}")

    return auroc, auprc

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Log both metrics for the model with imbalanced data

# CELL ********************

with mlflow.start_run(run_id=raw_run.info.run_id):
    auroc, auprc = evaluate(predictions)
    mlflow.log_metrics({"AUPRC": auprc, "AUROC": auroc})
    mlflow.log_params({"Data_Enhancement": "None", "DATA_FILE": DATA_FILE})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Log both metrics for the model with balanced data

# CELL ********************

with mlflow.start_run(run_id=smote_run.info.run_id):
    auroc, auprc = evaluate(smote_predictions)
    mlflow.log_metrics({"AUPRC": auprc, "AUROC": auroc})
    mlflow.log_params({"Data_Enhancement": "SMOTE", "DATA_FILE": DATA_FILE})

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Load

# MARKDOWN ********************

# ##### Register the 2 models using MLFlow

# CELL ********************

# Register the model
registered_model_name = f"{EXPERIMENT_NAME}-lightgbm"

raw_model_uri = "runs:/{}/model".format(raw_run.info.run_id)
mlflow.register_model(raw_model_uri, registered_model_name)

smote_model_uri = "runs:/{}/model".format(smote_run.info.run_id)
mlflow.register_model(smote_model_uri, registered_model_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Save the predictions result

# CELL ********************

from synapse.ml.predict import MLFlowTransformer

spark.conf.set("spark.synapse.ml.predict.enabled", "true")

model = MLFlowTransformer(
    inputCols=feature_cols,
    outputCol="prediction",
    modelName=f"{EXPERIMENT_NAME}-lightgbm",
    modelVersion=2,
)

test_spark = spark.createDataFrame(data=test, schema=test.columns.to_list())

batch_predictions = model.transform(test_spark)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Save the predictions to the lakehouse
batch_predictions.write.format("delta").mode("overwrite").save(f"{DATA_FOLDER}/predictions/batch_predictions2")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Synthetic adaptation

# CELL ********************

output = spark.read.format("delta").load("Tables/batch_predictions2")
display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

begin_day = "2026-07-21 00:00:00"

output = output.withColumn(
    "date_time",
    F.from_unixtime(F.unix_timestamp(F.lit(begin_day)) + F.col("Time")).cast("timestamp")
)

output = output.withColumn("Date", F.to_date("date_time"))

output = output.drop("date_time")

output = output.withColumnsRenamed(
    {
        "V1": "CustomerRiskScore",
        "V2": "TransactionVelocity",
        "V3": "MerchantTrustScore",
        "V4": "SpendingPatternIndex",
        "V5": "GeographicRisk",
        "V6": "DeviceRiskScore",
        "V7": "MerchantCategoryRisk",
        "V8": "CardUsageFrequency",
        "V9": "TransactionAnomalyScore",
        "V10": "BehavioralDeviation",
        "V11": "CustomerLoyaltyIndex",
        "V12": "FraudPatternScore",
        "V13": "AccountStability",
        "V14": "IdentityConfidence",
        "V15": "CustomerTenureScore",
        "V16": "HistoricalFraudRisk",
        "V17": "CardSecurityScore",
        "V18": "MerchantReputation",
        "V19": "TransactionConsistency",
        "V20": "SessionRiskScore",
        "V21": "PurchaseFrequency",
        "V22": "AverageSpendingIndex",
        "V23": "CrossBorderIndicator",
        "V24": "TimePatternScore",
        "V25": "LocationConsistency",
        "V26": "PaymentBehaviorScore",
        "V27": "DigitalActivityScore",
        "V28": "OverallRiskIndicator"
    }
)

all_cols = output.columns
all_cols.remove("Date")

output = output.select("Date", *all_cols)
display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

output = output.withColumns({
    "TransactionChannel":
        F.when(F.rand() < 0.55, "mobile_app")
        .when(F.rand() < 0.69, "atm")
        .when(F.rand() < 0.75, "online_banking")
        .when(F.rand() < 0.8, "api")
        .when(F.rand() < 0.88, "ecommerce")
        .when(F.rand() < 0.95, "in_person")
        .otherwise("pos"),
    "TransactionCountry":
        F.when(F.rand() < 0.50, "India")
        .when(F.rand() < 0.52, "Brazil")
        .when(F.rand() < 0.55, "Mexico")
        .when(F.rand() < 0.60, "United States")
        .when(F.rand() < 0.75, "Canada")
        .when(F.rand() < 0.78, "Spain")
        .when(F.rand() < 0.83, "Germany")
        .otherwise("Japan")
})

display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
begin_day = "2026-07-21 00:00:00"

output = output.withColumn(
    "Date_Time",
    F.from_unixtime(F.unix_timestamp(F.lit(begin_day)) + F.col("Time")).cast("timestamp")
)
display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.ml.feature import Bucketizer

splits = (output.select("Amount").approxQuantile("Amount", [i/10 for i in range(11)], 0.01))

bucketizer = Bucketizer(
    splits=splits,
    inputCol="Amount",
    outputCol="Amount_Bin"
)

output = bucketizer.transform(output)
display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import IntegerType
output = output.withColumn('Amount_Bin', F.col("Amount_Bin").cast(IntegerType()))
display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
output = output.withColumn(
    "Date_Time_Truncate",
    F.date_trunc("hour", F.col("Date_Time"))
)

display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

output = output.drop("Bins")
output = output.drop("Bins_label")
output = output.drop("Date_Time")
display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pyspark.sql.functions as F

df_columns = output.columns
df_columns.remove('Class')
df_columns.remove('prediction')

# Ensure that TARGET_COL is the last column
output = output.select(df_columns + ['Class', 'prediction']).withColumns({"Class": F.col('Class').cast("int"), "prediction": F.col('prediction').cast("int")})

display(output)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

output.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("batch_predictions")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# MARKDOWN ********************

# ##### 
