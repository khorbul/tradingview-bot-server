from flask import Flask, request, jsonify
import json
import requests
import os
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

app = Flask(__name__)

API_KEY = os.environ.get('PK3URU8NDWKD8FEMOFRS')
API_SECRET = os.environ.get('llEfnkpnYl27gHKlN2AJYmqcBkPyxmz2vckkhvvT')
BASE_URL = 'https://paper-api.alpaca.markets'


@app.route('/trade', methods=['POST'])
def place_order(action, symbol, quantity=1):
    try:
        alpaca_client = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_versio='v2')
        if action == 'BUY':
            buy_order = alpaca_client.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            return {"status": "buy order placed"}
        elif action == 'SELL':
            sell_order = alpaca_client.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            return {"status": "sell order placed"}
        else:
            return {"error": "Invalid action"}
    except Exception as e:
        return {"status": "failed", "reason": str(e)}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    if data is None:
        data = json.loads(request.data.decode('utf-8'))

    print(f"Received webhook data: {data}")
        
    action = data.get("action")
    symbol = data.get("symbol")
    quantity = data.get("quantity", 1)

    if action in ["BUY", "SELL"] and symbol:
        response = place_order(action, symbol, quantity)
        print(f"Alpaca API response: {response}")
        return jsonify(response)
    else:
        print("Error: Missing required fields in alert data.")
        return jsonify({"error": "Missing required fields in alert data"}), 400
@app.route('/')
def home():
    return "Trading Bot is live!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
