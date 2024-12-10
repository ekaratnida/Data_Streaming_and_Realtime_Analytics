import os
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime,timedelta,timezone
from bson import ObjectId  # Import ObjectId to check and convert
import pandas as pd
import time
import requests
import pendulum
from airflow.models import Variable

def on_failure_callback(**context):
    print(f"Task {context['task_instance_key_str']} failed.")

len = 5
   
def predictBTC(ti, **kwargs):  # Accept 'ti' as a direct argument
    
    counter = int(Variable.get("task_execution_counter", default_var=0))
   
    #Execute once per ten times 
    if counter%len == 0:
    
        import pickle
        
        modelFile = '/usr/local/airflow/tests/model.pkl'
        print(modelFile)
        
        # save
        with open(modelFile, 'rb') as f:
            clf = pickle.load(f)
        
        time_list = []
        current_timestamp_ms = int(time.time() * 1000)
       
        for i in range(1,len):
            print("i ",i)
            current_timestamp_ms = current_timestamp_ms + (60 * i * 1000)
            time_list.append(current_timestamp_ms)
        
        df = pd.DataFrame({'closeTime':time_list})
        print("df = ",df.head())
        
        y_hat = clf.predict(df['closeTime'].to_frame())
        print("y_hat = ",y_hat)
        
        df['predicted'] = y_hat
        df.to_csv('/usr/local/airflow/tests/out.csv', index=False)  

    # Increment the counter
    #counter += 1
    
    # Update the variable
    print(f"Task has been executed {counter} times.")
 
def evaluateModel(**kwargs):
    
    
    counter = int(Variable.get("task_execution_counter", default_var=0))
    print("counter = ",counter)
    errorList = Variable.get("error_list", default_var="[]")
    errorList = json.loads(errorList)
    
    if counter != 0 and counter%len != 0:
        url = 'https://api.binance.com/api/v3/ticker?type=MINI&symbol=BTCUSDT&windowSize=1h'
        response = requests.get(url)
        data = response.json()
        print(data)
        
        # Check if the file exists
        file_path = '/usr/local/airflow/tests/out.csv'
        if os.path.exists(file_path):
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(file_path)
            print("CSV file loaded successfully.")
            print('predictedPrice=', df.loc[counter-1,'predicted'])  # Display the first few rows of the DataFrame
            print('lastPrice=',data['lastPrice'])
            y_hat = float(df.loc[counter-1,'predicted'])
            y_actual = float(data['lastPrice'])
            import math
            errorList.append(abs(y_hat-y_actual)/y_actual)
            print(errorList)
            Variable.set("error_list", json.dumps(errorList))
        else:
            print(f"File '{file_path}' does not exist.")
    else:
        mape_path = '/usr/local/airflow/tests/mape.txt'
        if os.path.exists(mape_path):
            print("Calculate MAPE Error")
            mape = (sum(errorList)/len)*100
            print('mape =',mape)
            errorList = []
            Variable.set("error_list", json.dumps(errorList))
            
            d = kwargs["execution_date"]
            d = d + timedelta(hours=7)
            print("d = ",d)
            with open(mape_path, 'a') as output:
                output.write(f"{d}, {mape}\n")
        else:
            print("First run")
            with open(mape_path, 'a') as output:
                output.write(f"time, mape\n")
    
    counter += 1
    
    if counter == len:
        counter = 0
    
    Variable.set("task_execution_counter", counter) 
    

local_tz = pendulum.timezone("Asia/Bangkok")

with DAG(
    dag_id="Predict_BTC_Price",
    schedule_interval="*/1 * * * *",
    start_date=datetime(2024, 12, 10, 0, 0, 0, tzinfo=local_tz),
    catchup=False,
    tags=["crypto"],
    default_args={
        "owner": "Ekarat",
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": on_failure_callback
    }
) as dag:
    
    t1 = PythonOperator(
        task_id="predictBTC",
        python_callable=predictBTC,
        provide_context=True,  # Enable context
    )
    
    t2 = PythonOperator(
        task_id="evaluateModel",
        python_callable=evaluateModel,
        provide_context=True,  # Enable context
    )

    t1
    t2