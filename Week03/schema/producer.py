# Producer
from confluent_kafka import Producer
from bson import json_util
import json

p = Producer({'bootstrap.servers':'localhost:8097,localhost:8098,localhost:8099'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print(f"Message produced: key = {(msg.key().decode())} value = {(msg.value().decode())}")
        
data = {
    "movieId": 3,
    "title": "Jaws3",
    "genres": "Action, Sci-Fi",
    "rating": 4.8
}

p.produce('movies-topic', key="c003", value=json.dumps(data, default=json_util.default).encode('utf-8'), callback=acked)
    
p.flush()

print("Finished.")