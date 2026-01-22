from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serializing_producer import SerializingProducer

# 1. Define the Avro Schema
avro_schema_str = """
{
  "namespace": "example.avro",
  "type": "record",
  "name": "Movie",
  "fields": [
    {"name": "movieId", "type": "int"},
    {"name": "title", "type": "string"},
    {"name": "genres", "type": "string"},
    {"name": "rating", "type": "double"}
  ]
}
"""

# 2. Setup Registry Client and Serializer
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)
avro_serializer = AvroSerializer(schema_registry_client, avro_schema_str)

# 3. Setup Producer
producer_conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.serializer': StringSerializer(),
    'value.serializer': avro_serializer
}

p = SerializingProducer(producer_conf)
        
data = {"movieId": 2, "title": "Inception2", "genres": "Action, Sci-Fi", "rating": 4.8}

# Produce - SerializingProducer handles encoding automatically
p.produce(topic='movies-avro-topic', key="movie_1", value=data)
p.flush()
print("Avro message produced.")