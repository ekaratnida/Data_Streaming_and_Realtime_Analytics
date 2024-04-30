from confluent_kafka import Consumer, KafkaError, KafkaException
from sklearn import metrics
from river import linear_model
from river import optim
from river import preprocessing
from river import metrics
import json

running = True

metric = metrics.ROCAUC()
scaler = preprocessing.StandardScaler()
optimizer = optim.SGD(lr=0.01)
log_reg = linear_model.LogisticRegression(optimizer)

y_true = []
y_pred = []

def processData(value,sc,mo):
    value = json.loads(value) #convert dict str to dict
    yi = value["y"]
    del value["y"]
    xi = value
    
    # Scale the features
    sc.learn_one(xi)
    xi_scaled = sc.transform_one(xi)

    # Test the current model on the new "unobserved" sample
    #yi_pred = mo.predict_proba_one(xi_scaled)
    yi_pred = mo.predict_one(xi_scaled)

    print("Actual",yi,"------- Predicted",int(yi_pred))
    
    mo = mo.learn_one(xi_scaled, yi)

    

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
                recv = msg.value().decode()
                processData(recv, scaler, log_reg)
    finally:
        # Close down consumer to commit final offsets.
        c.close()

c = Consumer({'bootstrap.servers':"44.222.204.15:29092,44.222.204.15:29093,44.222.204.15:29094",
              'group.id':'group12',
			  'auto.offset.reset':'earliest'})
              
basic_consume_loop(c,['ekarat'])