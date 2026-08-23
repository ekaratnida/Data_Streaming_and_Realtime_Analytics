from confluent_kafka import Producer 
from confluent_kafka.schema_registry import SchemaRegistryClient 
from confluent_kafka.schema_registry.avro import AvroSerializer 
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField 
 
# Setup Client 
sr_client = SchemaRegistryClient({'url': 'http://localhost:8081'}) 
subject = 'movies-avro-topic-value' #topic name - value 
 
# PULL SCHEMA VERSION 1 FROM REGISTRY 
v1_meta = sr_client.get_version(subject, version=1) 
v1_schema_str = v1_meta.schema.schema_str 
print(v1_schema_str) 
print(f"Producer pulled Schema Version: {v1_meta.version}") 
 
# Setup Producer 
producer = Producer({'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099'}) 
avro_serializer = AvroSerializer(sr_client, v1_schema_str) 
string_serializer = StringSerializer('utf_8') 
 
# Data matching V1 (id, name) 
data = {"movieId": 2, "title": "Inception2", "genres": "Action, Sci-Fi", "rating": 4.8} 
producer.produce( 
    topic='movies-avro-topic', 
    key=string_serializer('movie_1'), 
    value=avro_serializer(data, SerializationContext('movies-avro-topic', MessageField.VALUE)) 
) 
 
producer.flush() 
print("Sent V1 message to Kafka.") 