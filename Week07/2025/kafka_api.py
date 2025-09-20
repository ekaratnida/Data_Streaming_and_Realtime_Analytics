# kafka_api.py
from fastapi import FastAPI
from kafka import KafkaConsumer
import json

app = FastAPI()

# Kafka consumer configuration
consumer = KafkaConsumer(
    'MOVIE_COUNT2',# replace with your topic
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='grafana-consumer',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Store recent messages in memory
messages = []

# Consume messages in background
import threading
def consume():
    for message in consumer:
        messages.append(message.value) #message.key
        # Keep only last 10 messages
        if len(messages) > 10:
            messages.pop(0)

threading.Thread(target=consume, daemon=True).start()

# API endpoint for Grafana
@app.get("/messages")
def get_messages():
    return {"data": messages}
