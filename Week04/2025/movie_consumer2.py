from confluent_kafka import Consumer
import json
import pandas as pd

running = True

import mysql.connector
connection = mysql.connector.connect(host="localhost",database="connect_test2",user="confluent2",password="confluent2", port=3307)

def basic_consume_loop(c, topics):
    try:
        c.subscribe(topics)

        while running:
            msg = c.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                results = json.loads(msg.value().decode())
                print(results)

                insert_cmd = f"insert into movie_tb (title, sale_ts, ticket_total_value) values ('{results['title']}','{results['sale_ts']}','{results['ticket_total_value']}')"

                print(insert_cmd)
                cursor = connection.cursor() #Should this line be called once?
                cursor.execute(insert_cmd)
                connection.commit()
    finally:
        # Close down consumer to commit final offsets.
        c.close()

def shutdown():
    running = False

c = Consumer({'bootstrap.servers':'localhost:8097',
              	'group.id':'group1',
		'auto.offset.reset':'earliest'})
              
basic_consume_loop(c,['movie'])
