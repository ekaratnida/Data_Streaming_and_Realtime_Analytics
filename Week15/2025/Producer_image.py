#install 
# pip install confluent_kafka

# Producer
from confluent_kafka import Producer
import time
import random
p = Producer({'bootstrap.servers':'10.10.83.206:8097'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (msg.value().decode()))

topic_name = 'image-topic'
image_path = 'receipt1.png'

# Read the PNG file in 'rb' (read binary) mode
with open(image_path, 'rb') as f:
    image_bytes = f.read()

# Send the raw bytes to Kafka
producer.send(topic_name, key=image_path, value=image_bytes, callback=acked)
producer.flush()

print(f"Sent {image_path} to topic {topic_name}")

