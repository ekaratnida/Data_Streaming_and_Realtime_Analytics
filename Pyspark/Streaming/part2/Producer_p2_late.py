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

event_time = time.time()  # or use a real event timestamp
message_text = "cat dog dog dog"

# Create a 2-column value (as JSON or CSV string)
# Option 1: JSON format (recommended for structured data)

# Option 2: CSV-like plain string (if you prefer simpler format)
# value = f"{event_time},{message_text}"
# eventTimeList = ["12:02","12:03","12:07","12:04","12:13"]
msgList = ["cat dog", "dog dog", "owl cat", "dog", "owl"]
# msgList = ["a", "b", "c", "d", "e"]

#for et, m in zip(eventTimeList, msgList):
#    dateime.now() - timedelta(seconds=10)
for i, m in enumerate(msgList):
    print(i)
    now = datetime.now().strftime("%H:%M:%S")
    # Implement late situation when i==3
    if i == 3:
        now = datetime.now() - timedelta(seconds=20)
        now = now.strftime("%H:%M:%S")
    print(now)
    value = json.dumps({
        "event_time": now,
        "message": m
    })
    p.produce('input', key="key", value=value, callback=acked)
    time.sleep(5) #random.randint(1,5))    
    p.poll(1)

    
