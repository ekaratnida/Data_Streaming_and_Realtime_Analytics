from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro import CachedSchemaRegistryClient
import random
from datetime import datetime
import time

# Set up schema registry client
schema_registry = CachedSchemaRegistryClient('http://localhost:8081')  # Change this to your Schema Registry URL

# Define the Avro schema
schema_str = '''
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
'''

# Define the Avro producer
avro_producer = AvroProducer(
    {
        'bootstrap.servers': 'localhost:9092',  # Change this to your Kafka broker address
        'schema.registry.url': 'http://localhost:8081',  # Change this to your Schema Registry URL
    },
    default_value_schema=schema_str
)

topic = 'movie'

# Generate sample records
titles = ["ET", "Hulk", "Spiderman"]
prices = [12, 24, 36]


# Produce records to Kafka
for _ in range(5):
    
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    record = {
        'title': random.choice(titles),
        'sale_ts': current_time,
        'ticket_total_value': random.choice(prices),
    }
    
    avro_producer.produce(topic=topic, value=record)
    print(f"Produced record: {record}")
    time.sleep(random.randint(1,2))

avro_producer.flush()
