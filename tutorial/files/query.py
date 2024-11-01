import requests
import json
import pandas as pd

url = "http://ec2-47-128-152-76.ap-southeast-1.compute.amazonaws.com:8099/query/sql"

headers = {
    "Content-Type": "application/json"
}
data = {
    "sql": "SELECT * FROM moviesSchema LIMIT 10"
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))
#print(response)

# Check the response status
if response.status_code == 200:
    # Convert the response to a Pandas DataFrame
    result = response.json()
    #print(result)
    columns = result['resultTable']['dataSchema']['columnNames']
    rows = result['resultTable']['rows']
    df = pd.DataFrame(rows, columns=columns)
    print(df)
else:
    print(f"Error: {response.status_code}, {response.text}")
    
#curl -X POST http://ec2-47-128-152-76.ap-southeast-1.compute.amazonaws.com:8099/query/sql -H "Content-Type: application/json" -d "{\"sql\":\"SELECT * FROM moviesSchema LIMIT 10\"}"
