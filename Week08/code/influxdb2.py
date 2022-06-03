import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

token = "-mUc7nLjHo97J84KXOJMiTu3gN_iIYlcbOnsngXGKohUY0Ijo9uWPXjRw9g9-0grGBEpiCR9T8QujSpRS59dYQ=="
org = "nida"
bucket = "nida"
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

import time
import random
while True:
    
    time.sleep(5) # Delay for 1 minute (60 seconds).

    randomlist = random.sample(range(10, 30), 1)
    print(randomlist)
    p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", float(randomlist[0]))
    write_api.write(bucket=bucket, org=org, record=p)

'''
query_api = client.query_api()
query = 'from(bucket:"nida")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn: (r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "temperature" )'
result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

print(results)
'''