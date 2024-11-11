from flask import Flask, request, jsonify
import requests
import os
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

app = Flask(__name__)

API_KEY = "AKZOGG3HQNJNWIHK6L69"
API_SECRET = "UI9tHyEYGZVWyLOdPTY5WUGJfaZzEeYxcFHxE58M"
alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')

@app.route('/trade', methods=['POST'])
def place_order(action, symbol, quantity=1):
    try:
        alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')
        if action == 'BUY':
            alpaca_client.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            return {"status": "buy order placed"}
        elif action == 'SELL':
            alpaca_client.submit_order(
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
