from confluent_kafka import Producer
import time

p = Producer({'bootstrap.servers': 'ec2-13-229-46-113.ap-southeast-1.compute.amazonaws.com:9092'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}'.format(msg.value().decode('utf-8')))

file1 = open('message.txt', 'r') 
Lines = file1.readlines()

for line in Lines:
    p.poll(0)
    sendMsg = line.encode().decode('utf-8').strip('\n')
    
    p.produce('my-first-topic', key="id1", value=sendMsg , callback=delivery_report)
    time.sleep(1)

p.flush()