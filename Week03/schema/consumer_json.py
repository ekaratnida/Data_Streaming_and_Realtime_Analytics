from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.deserializing_consumer import DeserializingConsumer

sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)


# 1. Setup JSON Deserializer
# We pass None for the schema because it will be fetched from the Registry
json_deserializer = JSONDeserializer(schema_str=None, 
                                     schema_registry_client=schema_registry_client)

# 2. Setup Consumer
consumer_conf_json = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.deserializer': StringDeserializer(),
    'value.deserializer': json_deserializer,
    'group.id': 'json-group',
    'auto.offset.reset': 'earliest'
}

consumer_json = DeserializingConsumer(consumer_conf_json)
consumer_json.subscribe(['movies-json-topic'])

print("Waiting for JSON Schema messages...")

try:
    while True:
        msg = consumer_json.poll(1.0)
        if msg is None: continue
        
        movie = msg.value()
        print(f"Consumed JSON Movie: {movie['title']} rated {movie['rating']}")
except KeyboardInterrupt:
    pass
finally:
    consumer_json.close()