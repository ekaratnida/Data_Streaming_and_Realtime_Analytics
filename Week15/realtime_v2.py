import dash
import dash_html_components as html
import dash_core_components as dcc
import requests
import datetime
from dash.dependencies import Input, Output

#Document of Binance API
#https://binance-docs.github.io/apidocs/spot/en/#rolling-window-price-change-statistics

coin = 'BTCUSDT'
tick_interval = '15m'
key = "https://api.binance.com/api/v3/ticker?symbol="+coin+"&windowSize="+tick_interval


figure = dict(
    data=[{'x': [], 'y': []}], 
    layout=dict(
        xaxis=dict(range=[]), 
        yaxis=dict(range=[16400, 16500])
        )
    )

app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title

app.layout = html.Div(
        [
            dcc.Graph(id='graph', figure=figure), 
            dcc.Interval(id="interval")
        ]
    )

@app.callback(
    Output('graph', 'extendData'), 
    [Input('interval', 'n_intervals')])
def update_data(n_intervals):

    print("interval ",n_intervals)

    data = requests.get(key)  
    data = data.json()
    print(data)

    price = float(data['lastPrice']) #price
    print(price)

    closeTime = data['closeTime']
    print(closeTime)

    my_datetime = datetime.datetime.fromtimestamp(closeTime / 1000)  # Apply fromtimestamp function
    print(my_datetime)             

    return dict(x=[[my_datetime]], y=[[price]])
    
if __name__ == '__main__':
    app.run_server()