#install 
# pip install confluent_kafka

# Producer
from confluent_kafka import Producer
import time
import random
p = Producer({'bootstrap.servers':'127.0.0.1:8097'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (msg.value().decode()))

msgList = ["cat dog dog dog", "owl cat", "dog owl"]

for m in msgList:
    p.produce('input', key="key", value=m, callback=acked)
    time.sleep(5) #random.randint(1,5))    
    p.poll(1)
    