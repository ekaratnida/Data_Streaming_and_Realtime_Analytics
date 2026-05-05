#install 
# pip install confluent_kafka

# Producer
from confluent_kafka import Producer
import time
import random
p = Producer({'bootstrap.servers':'192.168.1.124:8097'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (msg.value().decode()))

msgList = ["My cat is good.", "My dog is bad.", "My dog is an animal.", "Bangkok is beautiful city."]

for m in msgList:
    p.produce('input', key="key", value=m, callback=acked)
    p.poll(1)
    time.sleep(5)   
    