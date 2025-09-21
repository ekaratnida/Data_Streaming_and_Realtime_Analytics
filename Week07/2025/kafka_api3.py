# First, you need to install the necessary libraries:
# pip install fastapi uvicorn "kafka-python[avro]" fastavro

from fastapi import FastAPI
from kafka import KafkaConsumer
from io import BytesIO
import fastavro
import threading
import json

app = FastAPI()

# 1. Define your Avro Schema as a JSON string
# This schema must match the schema used by the Kafka producer that is sending the data.
MOVIE_COUNT_SCHEMA_JSON = """
{
    "connect.name": "io.confluent.ksql.avro_schemas.KsqlDataSourceSchema",
    "fields": [
        {
            "default": null,
            "name": "TICKETS_SOLD",
            "type": [
                "null",
                "long"
            ]
        }
    ],
    "name": "KsqlDataSourceSchema",
    "namespace": "io.confluent.ksql.avro_schemas",
    "type": "record"
}
"""

# Parse the JSON schema string into a Python dictionary for fastavro
try:
    # First, load the string as a Python dict
    schema_dict = json.loads(MOVIE_COUNT_SCHEMA_JSON)

    # Remove the Confluent-specific metadata field, as it's not part of the Avro spec
    # and can sometimes cause issues with parsers.
    if "connect.name" in schema_dict:
        del schema_dict["connect.name"]

    # Use fastavro's dedicated function to parse and validate the schema
    PARSED_SCHEMA = fastavro.parse_schema(schema_dict)
except (json.JSONDecodeError, Exception) as e:
    print(f"Error parsing or preparing Avro schema: {e}")
    PARSED_SCHEMA = {}


# 2. Create a deserializer function for Avro from a Schema Registry
def avro_deserializer(serialized_data):
    """
    Deserializes Avro binary data that was serialized using a schema registry.
    It strips the 5-byte prefix (magic byte + schema ID) before deserializing.
    """
    if not serialized_data:
        return None
    
    # Messages from producers using a Schema Registry are prefixed with:
    # - 1 Magic Byte (value 0)
    # - 4 bytes for the Schema ID
    # We must skip these first 5 bytes to get the actual Avro payload.
    if len(serialized_data) <= 5:
        print("Error: Serialized data is too short.")
        return None
    
    payload = serialized_data[5:]
    
    # Wrap the binary payload in a file-like object
    bytes_reader = BytesIO(payload)
    
    try:
        # Use fastavro to read the schemaless binary data with the parsed schema
        record = fastavro.schemaless_reader(bytes_reader, PARSED_SCHEMA)
        return record
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error deserializing Avro message: {e}")
        return None

# Kafka consumer configuration
consumer = KafkaConsumer(
    'MOVIE_COUNT',  # Replace with your topic
    bootstrap_servers='localhost:9092', # Corrected port for many Kafka setups
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='grafana-consumer-avro-2', # Changed group_id to reset offset
    # 3. Use the updated Avro deserializer
    value_deserializer=avro_deserializer
)

# Store recent messages in memory
messages = []

# Consume messages in the background
def consume():
    """
    A background thread function to continuously consume messages from Kafka.
    """
    print("Starting Kafka consumer thread...")
    for message in consumer:
        if message.value:
            print(f"Received message: {message.value}")
            messages.append(message.value)
            # Keep only the last 10 messages to avoid using too much memory
            if len(messages) > 10:
                messages.pop(0)
    print("Kafka consumer thread stopped.")

# Start the consumer thread
# The 'daemon=True' ensures the thread will exit when the main program exits.
consumer_thread = threading.Thread(target=consume, daemon=True)
consumer_thread.start()

# API endpoint for Grafana or any other client
@app.get("/messages")
def get_messages():
    """
    API endpoint to retrieve the most recent messages consumed from Kafka.
    """
    return {"data": messages}

# To run this application:
# 1. Save the code as main.py
# 2. Run the command: uvicorn main:app --reload