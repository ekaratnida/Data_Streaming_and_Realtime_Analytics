import requests
def get_btc_price():
        try:
            #response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=10)
            response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT',timeout=10)
            data = response.json()
            #print(data)
            #btc_price = float(data['bitcoin']['usd'])
            btc_price = float(data['price'])
            return btc_price
        except Exception as e:
            print(f"Error fetching BTC price: {e}")
            return None
        
from river import drift
from river import time_series, datasets, linear_model
from time import time, sleep

model = time_series.HoltWinters(
    alpha=0.3,
    beta=0.1,
    gamma=0.6,
    seasonality=12,
    multiplicative=True
)

# Initialize the drift detector
drift_detector = drift.ADWIN()
drifts = []


#dataset = datasets.AirlinePassengers().take(5)
#for i, v in dataset:
#    print(i," ",v)

model = linear_model.LinearRegression(intercept_lr=.1)
#print(dir(model))

#for i, val in enumerate(stream):
#for i in range(5):
i = 0
while True:
  #print(f"i={i}, val={val}")
  val = get_btc_price()
  print(val)

  #model.learn_one(val)
  #print(model.forecast(i))
  if i<11:
      print("Learning process...")
      model.learn_one({i:i},val)
  else:
      print(f"Predicted result {model.predict_one({i:i})}")
 
  drift_detector.update(val)   # Data is processed one sample at a time
  if drift_detector.drift_detected:
      # The drift detector indicates after each sample if there is a drift in the data
      print(f'Change detected at index {i}')
      drifts.append(i)
  sleep(5)
  i=i+1