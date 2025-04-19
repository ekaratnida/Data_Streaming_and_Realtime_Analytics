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
#eventTimeList = ["12:02","12:03","12:07","12:11","12:13"]
msgList = ["cat dog", "dog dog", "owl cat", "dog", "owl"]

#for et, m in zip(eventTimeList, msgList):
for m in msgList:
    now = datetime.now().strftime("%H:%M:%S")
    value = json.dumps({
        "event_time": now,
        "message": m
    })
    p.produce('input', key="key", value=value, callback=acked)
    time.sleep(3) #random.randint(1,5))    
    p.poll(1)
    