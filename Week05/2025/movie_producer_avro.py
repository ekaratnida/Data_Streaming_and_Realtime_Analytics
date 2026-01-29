from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import random
from datetime import datetime
import time

# 1. Setup Schema Registry Client explicitly
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)

# 2. Define Schema
schema_str = """
{
    "type": "record",
    "name": "TicketSale",
    "namespace": "test",
    "fields": [
        {"name": "title", "type": "string"},
        {"name": "sale_ts", "type": "string"},
        {"name": "ticket_total_value", "type": "int"}
    ]
}
"""

# 3. Create Avro Serializer
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

# 4. Define Producer with Serializer
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'value.serializer': avro_serializer
}
producer = SerializingProducer(producer_conf)

topic = 'movie'
titles = ["ET", "Hulk", "Spiderman"]
prices = [12, 24, 36]

for _ in range(5):
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    record = {
        'title': random.choice(titles),
        'sale_ts': current_time,
        'ticket_total_value': random.choice(prices),
    }
    
    # produce() handles the schema registration automatically here
    producer.produce(topic=topic, value=record)
    print(f"Produced record: {record}")
    time.sleep(random.randint(1,2))

producer.flush()