from confluent_kafka.schema_registry.json_schema import JSONSerializer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serializing_producer import SerializingProducer


# 1. Define the JSON Schema
json_schema_str = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Movie",
  "type": "object",
  "properties": {
    "movieId": {"type": "integer"},
    "title": {"type": "string"},
    "genres": {"type": "string"},
    "rating": {"type": "number"}
  },
  "required": ["movieId", "title"]
}
"""

# 2. Setup Serializer
# The lambda maps the data dict to the schema validation
sr_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(sr_conf)
json_serializer = JSONSerializer(json_schema_str, schema_registry_client)

# 3. Setup Producer
producer_conf_json = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'key.serializer': StringSerializer(),
    'value.serializer': json_serializer
}

p_json = SerializingProducer(producer_conf_json)

data = {"movieId": 2, "title": "Inception", "genres": "Action, Sci-Fi", "rating": 4.8}

# Produce
p_json.produce(topic='movies-json-topic', key="movie_1", value=data)
p_json.flush()
print("JSON Schema message produced.")