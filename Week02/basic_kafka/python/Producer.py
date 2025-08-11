#install 
#pip install confluent_kafka

# Producer
import time
from confluent_kafka import Producer
p = Producer({'bootstrap.servers':'localhost:8097,localhost:8098,localhost:8099'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print(f"Message produced: key = {(msg.key().decode())} value = {(msg.value().decode())}")

users = ["c001","c002"]
for i in range(20):
	p.produce('randomTopic', key=users[i%2], value="value_"+str(i), callback=acked)
	p.poll(1)
	time.sleep(1)