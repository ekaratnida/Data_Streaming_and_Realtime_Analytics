from confluent_kafka import Consumer
import json

# 1. Configure the Consumer
conf = {
    'bootstrap.servers': 'localhost:8097,localhost:8098,localhost:8099',
    'group.id': 'movie-readers',        # Identifies this consumer group
    'auto.offset.reset': 'earliest'     # Start reading from the beginning of the topic
}

c = Consumer(conf)

# 2. Subscribe to the topic
c.subscribe(['movies-topic'])

print("Waiting for messages... (Ctrl+C to stop)")

try:
    while True:
        # Poll for new messages (timeout of 1.0 second)
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # 3. Decode the key and value from bytes
        key = msg.key().decode('utf-8') if msg.key() else None
        value_raw = msg.value().decode('utf-8')
        
        # 4. Parse JSON back into a dictionary
        data = json.loads(value_raw)

        print(f"Received Key: {key}, Value: MovieID: {data['movieId']} | Title: {data['title']} | Rating: {data['rating']} | Genres: {data['genres']}.")

except KeyboardInterrupt:
    pass
finally:
    # 5. Clean up on exit
    c.close()