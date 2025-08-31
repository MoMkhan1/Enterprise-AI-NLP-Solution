"""
Spark Streaming Consumer for Kafka Financial Data + NLP
-------------------------------------------------------
Consumes messages from Kafka, parses JSON, performs simple analytics,
and optionally runs sentiment analysis on news headlines.
"""

import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType, DoubleType
from transformers import pipeline, AutoTokenizer, TFAutoModelForSequenceClassification

# -----------------------------
# Ensure Logs Folder Exists
# -----------------------------
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_FILE = os.path.join(LOGS_DIR, "spark_streaming.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Kafka + Spark Config
# -----------------------------
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "financial_data"
CHECKPOINT_DIR = "logs/spark_checkpoint"

# -----------------------------
# Initialize Spark Session
# -----------------------------
spark = SparkSession.builder \
    .appName("FinanceStreamingApp") \
    .getOrCreate()

spark.sparkContext
