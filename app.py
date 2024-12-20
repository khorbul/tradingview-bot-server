from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi

app = Flask(__name__)

API_KEY = 'PKE0HJBBRJSWI0SULDYB'
API_SECRET = 'cwdSuUQSwWID9jLtIQhNJID0UI08ASyUWZJnQVZg'
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        action = data.get('action')
        symbol = data.get('symbol')

        if action == 'BUY':
            buy_order = api.submit_order(
                symbol=symbol,
                qty=0.25,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            return jsonify({"status": "buy order placed", "order_id": buy_order.id})
        
        elif action == 'SELL':
            sell_order = api.submit_order(
                symbol=symbol,
                qty=0.25,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            return jsonify({"status": "sell order placed", "order_id": sell_order.id})
        else:
            return jsonify({"status": "no action taken", "reason": "invalid action"}), 400
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
