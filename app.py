from flask import Flask, request, jsonify
import requests
import os
from alpaca_trade_api.rest import REST, TimeFrame

app = Flask(__name__)

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')

def execute_trade(action, symbol):
    try:
        if action == "BUY":
            alpaca_client.submit_order(
                symbol=symbol,  # Stock symbol, e.g., 'AAPL' for Apple
                qty=1,          # Quantity to buy
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Market BUY order placed for {symbol} at {price}")
        elif action == "SELL":
            alpaca_client.submit_order(
                symbol=symbol,  # Stock symbol, e.g., 'AAPL' for Apple
                qty=1,          # Quantity to sell
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print(f"Market SELL order placed for {symbol} at {price}")
        else:
            print("Invalid action received")
    except Exception as e:
        print(f"Error placing order: {e}")

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
