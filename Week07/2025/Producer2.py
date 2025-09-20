#install 
#python -m pip install confluent_kafka

# Producer
import time
from confluent_kafka import Producer
import json
import random
from datetime import datetime
from bson import json_util 
p = Producer({'bootstrap.servers':'localhost:9092'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print(f"Message produced: key = {(msg.key().decode())} value = {(msg.value().decode())}")

movie_title = ['Unfrosted','Family Switch','Twisters']
sale_ts = None
ticket_total_value = [10,12,14]
for i in range(10000):
    data = {
        'title':random.choice(movie_title),
        'sale_ts':datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'ticket_total_value':random.choice(ticket_total_value)
    }
    p.produce('movie-ticket-sales',key="", 
                value=json.dumps(data,default=json_util.default).encode('utf-8'), 
                callback=acked)
    p.poll(1)
    time.sleep(2)