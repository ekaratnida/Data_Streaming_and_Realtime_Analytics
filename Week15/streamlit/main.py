import streamlit as st
import clickhouse_connect

st.title("Hello")

client = clickhouse_connect.get_client(
    host='d067qdw50x.ap-southeast-1.aws.clickhouse.cloud',
    user='default',
    password='4Fl8b.j~u9II4',
    secure=True
)

#st.info(client.command("show databases;"))

#st.info("Result:", client.command("SELECT count() FROM default.trips"))
#client.command('CREATE TABLE new_table (key UInt32, value String, metric Float64) ENGINE MergeTree ORDER BY key')
#row1 = [1000, 'String Value 1000', 5.233]
#row2 = [2000, 'String Value 2000', -107.04]
#data = [row1, row2]
#client.insert('new_table', data, column_names=['key', 'value', 'metric'])

sv = st.slider("limit",1,100,50)

result1 = client.query(f'SELECT * FROM trips limit {sv}')

@st.cache_data
def func():
    st.dataframe(result1.result_rows)

result2 = client.query('''SELECT
                                pickup_ntaname,
                                toHour(pickup_datetime) as pickup_hour,
                                SUM(1) AS pickups
                            FROM trips
                            WHERE pickup_ntaname != ''
                            GROUP BY pickup_ntaname, pickup_hour
                            ORDER BY pickup_ntaname, pickup_hour
                            limit 10 ''')

#st.info(len(result2.result_rows))
st.line_chart(result2.result_rows)