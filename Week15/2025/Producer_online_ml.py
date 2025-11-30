#install 
# pip install confluent_kafka

# Producer
from confluent_kafka import Producer
import time
from datetime import datetime, timedelta
import json
p = Producer({'bootstrap.servers':'127.0.0.1:8097'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (msg.value().decode()))

#event_time = time.time()  # or use a real event timestamp
labelList = [1,0,None]
textList = ["My cat is good.", "My dog is bad.", "My bad is good."]

for t, y in zip(textList, labelList):
    value = json.dumps({
        "text": t,
        "label": y
    })
    p.produce('input', key="key", value=value, callback=acked)
    time.sleep(5) #random.randint(1,5))    
    p.poll(1)
    