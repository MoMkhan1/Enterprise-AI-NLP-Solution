from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'nlp_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='test_group'
)

for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")
    break  # stop after first message
