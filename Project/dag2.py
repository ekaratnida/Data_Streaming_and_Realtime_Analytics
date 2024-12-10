import os
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime,timedelta
from bson import ObjectId  # Import ObjectId to check and convert
import pandas as pd
import pendulum
def on_failure_callback(**context):
    print(f"Task {context['task_instance_key_str']} failed.")

def downloadFromMongo(ti, **kwargs):
    try:
        hook = MongoHook(mongo_conn_id='mongo_default')
        client = hook.get_conn()
        db = client.MyDB
        btc_collection = db.btc_collection
        print(f"Connected to MongoDB - {client.server_info()}")

        # Convert ObjectId to string
        def convert_object_id(data):
            if isinstance(data, list):
                return [convert_object_id(item) for item in data]
            elif isinstance(data, dict):
                return {key: convert_object_id(value) for key, value in data.items()}
            elif isinstance(data, ObjectId):
                return str(data)
            else:
                return data

        # Fetch and convert data
        raw_data = list(btc_collection.find())
        converted_data = convert_object_id(raw_data)
        results = json.dumps(converted_data)
        print(results)

        ti.xcom_push(key="data", value=results)  # Use 'ti' to push to XCom

    except Exception as e:
        print(f"Error connecting to MongoDB -- {e}")

def trainModel(ti, **kwargs):  # Accept 'ti' as a direct argument
    data = ti.xcom_pull(
        task_ids="Get_BTC_from_Mongodb",  # Correct task_id
        key="data"
    )
    print("Get data for training:", data)
    df = pd.DataFrame(json.loads(data))
    print(df.head())
    
    from sklearn.linear_model import LinearRegression
    X = df[["closeTime"]]
    y = df["lastPrice"]
    reg = LinearRegression()
    reg.fit(X, y)
    print(reg.score(X, y))
    print(reg.coef_)
    print(reg.intercept_)

    print("Path at terminal when executing this file")
    print(os.getcwd() + "\n")
    
    import pickle
    import time
    # save
    current_timestamp_ms = int(time.time() * 1000)
    modelFile = '/usr/local/airflow/tests/model.pkl'
    print(modelFile)
    
    # save
    with open('/usr/local/airflow/tests/model.pkl','wb') as f:
        pickle.dump(reg,f)

local_tz = pendulum.timezone("Asia/Bangkok")
with DAG(
    dag_id="Train_ML_Model",
    schedule_interval= "0 */1 * * *",
    start_date=datetime(2024, 12, 10, tzinfo=local_tz),
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
        task_id="Get_BTC_from_Mongodb",
        python_callable=downloadFromMongo,
        provide_context=True,  # Enable context
    )

    t2 = PythonOperator(
        task_id="train_model",
        python_callable=trainModel,
        provide_context=True,  # Enable context
    )

    t1 >> t2