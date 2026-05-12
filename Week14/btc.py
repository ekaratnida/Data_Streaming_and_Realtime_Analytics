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
from time import time, sleep

# Initialize the drift detector

drift_detector = drift.ADWIN()
drifts = []

#for i, val in enumerate(stream):
#for i in range(10):
while True:
  #print(f"i={i}, val={val}")
  val = get_btc_price()
  print(val)
  drift_detector.update(val)   # Data is processed one sample at a time
  if drift_detector.drift_detected:
      # The drift detector indicates after each sample if there is a drift in the data
      print(f'Change detected at index {i}')
      drifts.append(i)
  sleep(10)