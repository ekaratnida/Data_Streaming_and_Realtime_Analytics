from confluent_kafka import Consumer 
from confluent_kafka.schema_registry import SchemaRegistryClient 
from confluent_kafka.schema_registry.avro import AvroDeserializer 
from confluent_kafka.serialization import SerializationContext, MessageField 
 
# Setup Client 
sr_client = SchemaRegistryClient({'url': 'http://localhost:8081'}) 
subject = 'movies-avro-topic-value' 
 
# PULL THE LATEST SCHEMA (Version 2) FROM REGISTRY 
latest_meta = sr_client.get_latest_version(subject) 
v2_schema_str = latest_meta.schema.schema_str 
print(v2_schema_str)
 
print(f"Consumer pulled Latest Schema Version: {latest_meta.version}") 
 
# Setup Consumer 
consumer = Consumer({ 
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099', 
    'group.id': 'backward-test-group', 
    'auto.offset.reset': 'earliest' 
}) 

consumer.subscribe(['movies-avro-topic']) 
 
# The Deserializer uses V2 to read whatever comes from the wire 
avro_deserializer = AvroDeserializer(sr_client, v2_schema_str) 
 
try: 
    while True: 
        msg = consumer.poll(1.0) 
        if msg is None: continue 
         
        movie = avro_deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)) 
        print(f"Consumed Avro Movie: {movie}")

except KeyboardInterrupt: 
    pass 
finally: 
    consumer.close() 