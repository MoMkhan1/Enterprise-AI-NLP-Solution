"""
Kafka Producer for Finance Projects
-----------------------------------
Reads CSV from container path and sends each row as a message to Kafka with logging.
"""

from kafka import KafkaProducer
import logging
import json
import os
import pandas as pd

# -----------------------------
# Environment Variables
# -----------------------------
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "nlp_topic")
DATA_FILE = os.environ.get("CSV_PATH", "/app/data/finance_data.csv")  # Use container CSV_PATH

# -----------------------------
# Ensure Logs Folder Exists
# -----------------------------
LOGS_DIR = "/app/logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_FILE = os.path.join(LOGS_DIR, "kafka_producer.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Kafka Producer
# -----------------------------
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic: str, message: dict):
    try:
        producer.send(topic, message)
        producer.flush()
        logger.info(f"Sent message to topic '{topic}': {message}")
        print(f"✅ Message sent to '{topic}': {message}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        print(f"❌ Error sending message: {e}")

# -----------------------------
# Load CSV and Send Messages
# -----------------------------
if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        print(f"❌ Data file not found: {DATA_FILE}")
        exit(1)

    df = pd.read_csv(DATA_FILE)
    print(f"📄 Loaded {len(df)} projects from CSV.")

    for idx, row in df.iterrows():
        message = {
            "project_id": int(row.get("project_id", idx + 1)),
            "project_name": row.get("project_name", "Unnamed Project"),
            "other_columns": row.to_dict()  # send all columns
        }
        send_message(KAFKA_TOPIC, message)

    print("✅ All projects sent to Kafka!")
