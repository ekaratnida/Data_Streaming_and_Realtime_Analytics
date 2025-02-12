from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
import random
from datetime import datetime
import time

# Kafka & Schema Registry Configuration
KAFKA_BROKER = "localhost:9092"
SCHEMA_REGISTRY_URL = "http://localhost:8081"
OUTPUT_TOPIC = 'movie-ticket-sales'

schema_registry_client = SchemaRegistryClient({'url': SCHEMA_REGISTRY_URL})

# Fetch schema from Schema Registry
schema_subject = f"{OUTPUT_TOPIC}-value"
schema_response = schema_registry_client.get_latest_version(schema_subject)
schema_str = schema_response.schema.schema_str


# Create Avro Serializer and Deserializer
avro_serializer = AvroSerializer(schema_registry_client, schema_str)

producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Generate sample records
titles = ["ET", "Hulk", "Spiderman"]
prices = [12, 24, 36]

# Produce records to Kafka
for _ in range(5):
    
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    record = dict(
        TITLE=random.choice(titles),
        SALE_TS=current_time,
        TICKET_TOTAL_VALUE=random.choice(prices)
    )

    serialized_value = avro_serializer(record, SerializationContext(OUTPUT_TOPIC, MessageField.VALUE))
    
    # Send to new topic
    producer.produce(topic=OUTPUT_TOPIC, key="movie", value=serialized_value)
    print(f"Produced record: {record}")
    producer.flush()
    time.sleep(random.randint(1,2))

