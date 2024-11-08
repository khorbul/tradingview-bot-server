from flask import Flask, request, jsonify
import requests
import os
from alpaca_trade_api.rest import REST, TimeFrame

alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')  # Use paper trading for testing

app = Flask(__name__)

# Add your trading platform API key and secret as environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

def execute_trade(action):
    try:
        if action == "BUY":
            order = alpaca_client.submit_order(
                symbol='NQ1!',  # Stock symbol, e.g., 'AAPL' for Apple
                qty=1,          # Quantity to buy
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print("Buy order placed:", order)
        elif action == "SELL":
            order = alpaca_client.submit_order(
                symbol='NQ1!',  # Stock symbol, e.g., 'AAPL' for Apple
                qty=1,          # Quantity to sell
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print("Sell order placed:", order)
    except Exception as e:
        print("An error occurred:", e)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data['action'] == "BUY":
        execute_trade("BUY")
    elif data['action'] == "SELL":
        execute_trade("SELL")
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
