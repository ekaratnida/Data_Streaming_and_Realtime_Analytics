from confluent_kafka import Producer
import json
import random
import time
from datetime import datetime
from bson import json_util

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (msg.value().decode()))

p = Producer({'bootstrap.servers':'localhost:8097'})

titles = ["ET", "Hulk", "Spiderman"]
prices=[12,24,36]

for i in range(10):

    current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    data = {
        'title': random.choice(titles),
        'sale_ts': current_time,
        'ticket_total_value': random.choice(prices)
    }

    p.produce('movie',
              key="key",
              value=json.dumps(data, default=json_util.default).encode('utf-8'),
              callback=acked)
    p.poll(1)
    time.sleep(random.randint(1,5))
