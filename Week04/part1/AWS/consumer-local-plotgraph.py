from confluent_kafka import Consumer

c = Consumer({
    'bootstrap.servers': 'ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'latest'
})

c.subscribe(['streams-pageviewstats-untyped-output'])
              
import matplotlib.pyplot as plt
#from matplotlib.pyplot import figure
#figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
#plt.ion()
lr = {}

import json

while True:
    msg = c.poll(0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    value = msg.value().decode()
    print(value)
    kvalue = msg.key().decode("utf-8", "ignore")
    print(kvalue)
    x = json.loads(kvalue)
    y = json.loads(value)
    print('Received message: {0} , {1}'.format(x["window-start"], y["count"]))
   
    plt.bar(x["region"], y["count"],color='r')
    plt.pause(1)
    

plt.show(block=True)
c.close()

