from confluent_kafka import Consumer, KafkaError, KafkaException
from sklearn import metrics
from river import linear_model
from river import optim
from river import stream
from river import preprocessing
from river import metrics
from river import evaluate
import json

running = True

metric = metrics.ROCAUC()
scaler = preprocessing.StandardScaler()
optimizer = optim.SGD(lr=0.01)
log_reg = linear_model.LogisticRegression(optimizer)

y_true = []
y_pred = []

def processData(value):
    
    value = json.loads(value) #convert dict str to dict
    yi = value["y"]
    del value["y"]
    xi = value
    
    # Scale the features
    scaler.learn_one(xi)
    xi_scaled = scaler.transform_one(xi)

    # Test the current model on the new "unobserved" sample
    yi_pred = log_reg.predict_proba_one(xi_scaled)
    #yi_pred = log_reg.predict_one(xi_scaled)
    #print(yi_pred)
    
    # Train the model with the new sample
    #log_reg.learn_one(xi_scaled, yi)
    
    #print("Actual y = ", yi)
    #print("Predicted y = ", 0 if yi_pred[True] < 0.1 else 1)
    metric = metric.update(yi, yi_pred)
    model = model.learn_one(xi_scaled, y)
    print(metric)
    
    #evaluate.progressive_val_score(dataset, log_reg, metric, print_every=10)
    

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
                processData(msg.value().decode())
    finally:
        # Close down consumer to commit final offsets.
        c.close()

c = Consumer({'bootstrap.servers':"44.222.204.15:29092,44.222.204.15:29093,44.222.204.15:29094",
              'group.id':'group2',
			  'auto.offset.reset':'earliest'})
              
basic_consume_loop(c,['cancer'])