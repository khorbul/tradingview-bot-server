from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import threading
import time
import os

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
BASE_URL = os.getenv('https://paper-api.alpaca.markets')
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def place_order():
    try:
        # Get the data from the incoming webhook
        data = request.json
        action = data.get('action')
        symbol = data.get('symbol')
        
        if action == 'BUY':
            # Submit the buy order
            buy_order = api.submit_order(
                symbol=symbol,
                qty=0.5,
                side='buy',
                type='market',
                time_in_force='gtc'
            )

            # Wait for the buy order to be filled
            filled_order = alpaca_client.get_order(buy_order.id)
            while filled_order.status != 'filled':
                filled_order = alpaca_client.get_order(buy_order.id)
                time.sleep(1) # Wait 1 second before checking again

            # Get the filled price
            buy_price = float(filled_order.filled_avg_price)

            # Calculate the sell price for $10 profit
            sell_price = buy_price + 10 # Adjust the $10 profit target

            # Submit the sell order at the calculated sell price
            sell_order = alpaca_client.submit_order(
                symbol='BTC/USD',
                qty=0.5, # Same quantity as the buy order
                side='sell',
                type='limit',
                limit_price=sell_price,
                time_in_force='gtc'
            )    

            # Print the buy price and the sell target
            print(f"Buy price: ${buy_price:.2f}")
            print(f"Sell order placed at ${sell_price:.2f} for $10 profit")

            return jsonify({"status": "Buy order placed", "sell_price": sell_price}), 200
        
        else:
            return jsonify({"status": "no action taken", "reason": "invalid action"}), 400
            
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
