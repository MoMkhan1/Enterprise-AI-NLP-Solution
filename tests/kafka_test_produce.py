from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
producer.send('nlp_topic', b'Hello from Python!')
producer.flush()
print("Message sent successfully!")
