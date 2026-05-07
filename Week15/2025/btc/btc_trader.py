import requests
import time
import random
import json
from datetime import datetime

class VirtualBTCTrader:
    def __init__(self, initial_usd=10000):
        self.usd_balance = initial_usd
        self.btc_balance = 0.0
        self.btc_price = 0.0
        self.transactions = []
        self.buy_lots = []
        self.realized_pnl = 0.0
        
    def get_btc_price(self):
        try:
            response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', timeout=10)
            data = response.json()
            self.btc_price = float(data['price'])
            return self.btc_price
        except Exception as e:
            print(f"Error fetching BTC price: {e}")
            return None
    
    def buy_btc(self, amount_usd):
        if amount_usd > self.usd_balance:
            print(f"Insufficient USD balance. Available: ${self.usd_balance:.2f}")
            return False
        
        btc_amount = amount_usd / self.btc_price
        self.usd_balance -= amount_usd
        self.btc_balance += btc_amount
        
        self.buy_lots.append({
            'btc_amount': btc_amount,
            'cost_basis': amount_usd,
            'price': self.btc_price
        })
        
        transaction = {
            'type': 'BUY',
            'timestamp': datetime.now().isoformat(),
            'price': self.btc_price,
            'usd_spent': amount_usd,
            'btc_received': btc_amount
        }
        self.transactions.append(transaction)
        print(f"BOUGHT: ${amount_usd:.2f} -> {btc_amount:.8f} BTC at ${self.btc_price:,.2f}")
        return True
    
    def sell_btc(self, btc_amount):
        if btc_amount > self.btc_balance:
            print(f"Insufficient BTC balance. Available: {self.btc_balance:.8f} BTC")
            return False
        
        usd_received = btc_amount * self.btc_price
        self.btc_balance -= btc_amount
        self.usd_balance += usd_received
        
        cost_basis = 0.0
        remaining_to_sell = btc_amount
        
        while remaining_to_sell > 0 and self.buy_lots:
            lot = self.buy_lots[0]
            if lot['btc_amount'] <= remaining_to_sell:
                cost_basis += lot['cost_basis']
                remaining_to_sell -= lot['btc_amount']
                self.buy_lots.pop(0)
            else:
                proportion = remaining_to_sell / lot['btc_amount']
                cost_basis += lot['cost_basis'] * proportion
                lot['btc_amount'] -= remaining_to_sell
                lot['cost_basis'] *= (1 - proportion)
                remaining_to_sell = 0
        
        gain_loss = usd_received - cost_basis
        self.realized_pnl += gain_loss
        
        transaction = {
            'type': 'SELL',
            'timestamp': datetime.now().isoformat(),
            'price': self.btc_price,
            'btc_sold': btc_amount,
            'usd_received': usd_received,
            'cost_basis': cost_basis,
            'gain_loss': gain_loss
        }
        self.transactions.append(transaction)
        print(f"SOLD: {btc_amount:.8f} BTC -> ${usd_received:.2f} at ${self.btc_price:,.2f} | P&L: ${gain_loss:+.2f}")
        return True
    
    def print_status(self):
        total_value = self.usd_balance + (self.btc_balance * self.btc_price)
        
        cost_basis = sum(lot['cost_basis'] for lot in self.buy_lots)
        unrealized_pnl = (self.btc_balance * self.btc_price) - cost_basis
        total_pnl = self.realized_pnl + unrealized_pnl
        
        print(f"\n{'='*50}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"BTC Price: ${self.btc_price:,.2f}")
        print(f"USD Balance: ${self.usd_balance:.2f}")
        print(f"BTC Balance: {self.btc_balance:.8f} BTC")
        print(f"Total Value: ${total_value:,.2f}")
        print(f"P&L: ${total_pnl:+.2f} (Realized: ${self.realized_pnl:+.2f} | Unrealized: ${unrealized_pnl:+.2f})")
        print(f"{'='*50}\n")
    
    def save_transactions(self):
        with open('transactions.json', 'w') as f:
            json.dump(self.transactions, f, indent=2)

def main():
    trader = VirtualBTCTrader(initial_usd=10000)
    print("Virtual BTC Trader Started")
    print("Press Ctrl+C to stop\n")
    
    has_position = False
    sell_time = None
    
    try:
        while True:
            price = trader.get_btc_price()
            if price is None:
                time.sleep(10)
                continue
            
            trader.print_status()
            
            if not has_position:
                buy_amount = 1000 #random.randint(500, 2000)
                if trader.buy_btc(buy_amount):
                    has_position = True
                    sell_time = time.time() + 30 #random.randint(30, 300)
                    print(f"Will sell in {int(sell_time - time.time())} seconds")
            else:
                if time.time() >= sell_time:
                        sell_amount = random.uniform(0.3, 1.0) * trader.btc_balance
                        if trader.sell_btc(sell_amount):
                            has_position = False
                            if random.random() < 0.3:
                                trader.sell_btc(trader.btc_balance)
                                has_position = False
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\nStopping trader...")
        trader.save_transactions()
        print(f"Transactions saved to transactions.json")
        print(f"Final balance: ${trader.usd_balance:.2f}")
        print(f"Final BTC: {trader.btc_balance:.8f} BTC")

if __name__ == "__main__":
    main()
