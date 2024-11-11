from flask import Flask, request, jsonify
import requests
import os
from alpaca_trade_api.rest import REST, TimeFrame

app = Flask(__name__)

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')

from alpaca_trade_api.rest import REST, TimeFrame

# Initialize the Alpaca API client
alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()
    symbol = data.get("symbol")
    action = data.get("action")  # "buy" or "sell"
    quantity = data.get("quantity")

    if action == "buy":
        alpaca_client.submit_order(symbol=symbol, qty=quantity, side='buy', type='market', time_in_force='gtc')
    elif action == "sell":
        alpaca_client.submit_order(symbol=symbol, qty=quantity, side='sell', type='market', time_in_force='gtc')

    return jsonify({"status": "order placed"}), 200

@app.route("/webhook", methods=['POST'])
def webhook():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "No data received"}), 400

    action = data.get('action', '')
    symbol = data.get('symbol', '')

    print(f"Received action: {action} for {symbol}")

    if action == 'BUY':
        place_order('buy', symbol)
    elif action == 'SELL':
        place_order('sell', symbol)
    else:
        return jsonify({"error": "Invalid action"}), 400

    return jsonify({"status": "success"}), 200

@app.route('/')
def home():
    return "Trading Bot is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
