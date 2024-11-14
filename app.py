from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi
import threading
import time

app = Flask(__name__)

API_KEY = 'PKCAXN5MUDCWCEK7XYC0'
API_SECRET = 'iexDDqoWlg10LhFDfjx7ZaRxXOMlboPVgmLTOpeL'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

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

            filled_order = api.get_order(buy_order.id)
            while filled_order.status != 'filled':
                filled_order = alpaca_client.get_order(buy_order.id)
                time.sleep(1)

            buy_price = float(filled_order.filled_avg_price)
            print(f"Buy price: ${buy_price:.2f}")

            sell_price = buy_price + 10

            take_profit_order = api.submit_order(
                symbol='BTC/USD',
                qty=0.5,
                side='sell',
                type='limit',
                limit_price=sell_price,
                time_in_force='gtc'
            )    

            print(f"Take Profit order placed at ${sell_price:.2f} for $10 profit")
        
        else:
            return jsonify({"status": "no action taken", "reason": "invalid action"}), 400
            
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
