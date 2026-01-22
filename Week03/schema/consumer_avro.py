from confluent_kafka import Consumer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.deserializing_consumer import DeserializingConsumer

# 1. Setup Registry Client
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)

# 2. Setup Avro Deserializer 
# the consumer pulls it from the Registry using the ID in the message.
avro_deserializer = AvroDeserializer(schema_registry_client)

# 3. Setup Consumer
consumer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.deserializer': StringDeserializer(),
    'value.deserializer': avro_deserializer,
    'group.id': 'avro-group',
    'auto.offset.reset': 'earliest'
}

consumer = DeserializingConsumer(consumer_conf)
consumer.subscribe(['movies-avro-topic'])

print("Waiting for Avro messages...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        movie = msg.value()
        print(f"Consumed Avro Movie: {movie['title']} ({movie['rating']})")

except KeyboardInterrupt:
    pass

finally:
    consumer.close()