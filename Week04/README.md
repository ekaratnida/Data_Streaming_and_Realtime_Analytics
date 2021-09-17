Outline

<!-- 1. Check homework
	- How long to get your answer?
	- What is your answer? -->

## 1. Review, Wordcount, Temperature (part 0)
   pip install confluent-kafka

## 2. PageViewDemo (part 1)
   1. Start kafka cluster --> double click "1_start_cluster.bat".
   2. Create a topic --> double click "2_create_pageview_topics.bat" --> Press 'Enter' when finish.
   3. Double click "3_2_run_python_consume_plotgraph.bat"
   4. Double click "4_compile_pageview_demo.bat"
   5. Double click "5_run_python_publish.bat"

## 3. More analytical methods (part 2)
	1. Part2/Sum
	2. Part2/Min max

## 4. Connect to Cloud (AWS)

VENV
- https://medium.com/@chanisarauttamawetin/virtual-environments-in-python-%E0%B9%83%E0%B8%8A%E0%B9%89%E0%B8%87%E0%B9%88%E0%B8%B2%E0%B8%A2%E0%B9%86%E0%B8%81%E0%B8%B1%E0%B8%9A-vscode-4d23d29dd57e
- pip install virtualenv
- virtualenv venv
- venv\Scripts\activate

Python:
- https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
- pip install kafka-python

```python
#Producer
from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['xxxx'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for e in range(1000):
    data = {
        'timestamp' : datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f'"),
        'number' : e
    }
    print(data)
    producer.send('quickstart-events', value=data)
    sleep(1)
```
```python
#Consumer
from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(
    'quickstart-events',
     bootstrap_servers=['xxxx'],
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    print(message)
```

## 5. Testing before real quiz
	1. Send data to all students
	2. Each of them analyze data and return to teacher
	
## TF-IDF
https://www.freecodecamp.org/news/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3/


## Reference

Json generator https://github.com/everwatchsolutions/json-data-generator

https://kafka.apache.org/21/javadoc/org/apache/kafka/streams/kstream/KStream.html

https://docs.confluent.io/platform/current/streams/faq.html
