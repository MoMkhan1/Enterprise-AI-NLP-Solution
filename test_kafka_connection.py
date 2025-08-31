from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic
import time

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "test_topic"

# Step 1: Create Admin Client
try:
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER,
        client_id="test_client"
    )
    print("✅ Connected to Kafka broker at", KAFKA_BROKER)

    # Step 2: Create Topic (if not exists)
    try:
        topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"✅ Topic '{TOPIC_NAME}' created")
    except Exception as e:
        print(f"⚠️ Topic creation skipped: {e}")

    # Step 3: Produce a test message
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    producer.send(TOPIC_NAME, b"Hello Kafka!")
    producer.flush()
    print("✅ Message produced to", TOPIC_NAME)

    # Step 4: Consume the test message
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="test_group"
    )
    print("🔄 Waiting for messages...")
    for message in consumer:
        print(f"✅ Consumed message: {message.value.decode()}")
        break  # Stop after first message

except Exception as e:
    print("❌ Kafka test failed:", e)
