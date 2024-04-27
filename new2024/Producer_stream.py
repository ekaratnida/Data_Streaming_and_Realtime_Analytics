
# Producer
from confluent_kafka import Producer
from time import sleep
from sklearn import datasets
from river import linear_model
from river import optim
from river import stream
from river import preprocessing
from bson import json_util
import json

p = Producer({'bootstrap.servers':"44.222.204.15:29092,44.222.204.15:29093,44.222.204.15:29094"})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (msg.value().decode()))

id = 1
for xi, yi in stream.iter_sklearn_dataset(datasets.load_breast_cancer(), shuffle=True, seed=42):
    
    print(type(xi))
    xi["y"] = str(yi)
    data = json.dumps(xi, default=json_util.default).encode('utf-8')
    print(type(data))
    p.produce('cancer', key = str(id), value = data, callback=acked)
    sleep(2)
    p.poll(1)
    id = id+1
    if id == 10:
        break
    

# Example of json schema
# https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/json_producer.py
