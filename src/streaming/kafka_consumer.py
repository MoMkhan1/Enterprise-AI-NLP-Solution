"""
Kafka Consumer with PostgreSQL Integration
------------------------------------------
Consumes messages from Kafka topic and inserts them into PostgreSQL.
"""

from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
import json
import os
import psycopg2
import time

# -----------------------------
# Environment Variables
# -----------------------------
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", 5432))
DB_NAME = os.environ.get("DB_NAME", "finance_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "admin")

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "nlp_topic")
KAFKA_GROUP = os.environ.get("KAFKA_GROUP", "nlp_group")

# -----------------------------
# Ensure Logs Folder Exists
# -----------------------------
LOGS_DIR = "/app/logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# -----------------------------
# Logging Configuration
# -----------------------------
LOG_FILE = os.path.join(LOGS_DIR, "kafka_consumer.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -----------------------------
# Kafka Consumer with Retry
# -----------------------------
consumer = None
for attempt in range(10):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=KAFKA_GROUP,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("🟢 Kafka consumer connected!")
        logger.info("Kafka consumer connected!")
        break
    except KafkaError as e:
        print(f"⚠️ Attempt {attempt+1}: Kafka broker not ready, retrying in 5 seconds...")
        logger.warning(f"Attempt {attempt+1}: Kafka broker not ready: {e}")
        time.sleep(5)
else:
    print("❌ Could not connect to Kafka broker. Exiting.")
    logger.error("Could not connect to Kafka broker. Exiting.")
    exit(1)

logger.info("Kafka consumer started...")
print("🟢 Kafka consumer started... Listening for messages.")

# -----------------------------
# Function to Insert into PostgreSQL
# -----------------------------
def insert_project_to_db(project):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id SERIAL PRIMARY KEY,
            project_name TEXT,
            other_columns JSONB
        )
        """)

        cursor.execute(
            "INSERT INTO projects (project_name, other_columns) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (project.get("project_name"), json.dumps(project.get("other_columns", {})))
        )
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Inserted project into DB: {project}")
        print(f"✅ Project inserted into DB: {project}")
    except Exception as e:
        logger.error(f"Error inserting project into DB: {e}")
        print(f"❌ Error inserting project into DB: {e}")

# -----------------------------
# Consume Messages
# -----------------------------
for message in consumer:
    project_data = message.value
    logger.info(f"Received message: {project_data}")
    print(f"📩 Received: {project_data}")

    insert_project_to_db(project_data)
