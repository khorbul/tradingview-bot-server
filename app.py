from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import threading
import time

app = Flask(__name__)

API_KEY = 'PKI1IQ3DZ61X4PXZC6ZV'
API_SECRET = 'Ksh3Ikomr2RC7TSlaOcIpcn50C74pdyBdDmYMuWr'
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

purchase_info = {}

def monitor_profit():
    while True:
        for symbol, avg_price in purchase_info.items():
            try:
                position = api.get_position(symbol)
                current_price = float(api.get_last_trade(symbol).price)
                profit = (current_price - avg_price) * float(position.qty)

                if profit >= 10:
                    sell_order = api.submit_order(
                        symbol=symbol,
                        qty=position.qty,
                        time='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                    print(f"Sell order placed for {symbol} with profit of ${profit:.2f}")

                    purchase_info.pop(symbol)
            except Exception as e:
                print(f"Error checking profit for {symbol}: {e}")
        
        time.sleep (1)

threading.Thread(target=monitor_profit, daemon=True).start()

@app.route('/webhook', methods=['POST'])
def place_order():
    try:
        data = request.json
        action = data.get('action')
        symbol = data.get('symbol')
        
        if action == 'BUY':
            buy_order = api.submit_order(
                symbol=symbol,
                qty=0.5,
                side='buy',
                type='market',
                time_in_force='gtc'
            )

            time.sleep(1)
            position = api.get_position(symbol)
            purchaase_info[symbol] = float(position.avg_entry_price)
            
            return jsonify({"status": "buy order placed", "order_id": buy_order.id})
        else:
            return jsonify({"status": "no action taken", "reason": "invalid action"}), 400
            
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
