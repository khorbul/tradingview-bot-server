from flask import Flask, request, jsonify
import requests
import os
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

app = Flask(__name__)

API_KEY = "PKLR99QFR0NBIQ85S2HY"
API_SECRET = "O3zBUBz8f9GksEWtDN70Ujd4rbvnKZa7frBgh73u"

@app.route('/trade', methods=['POST'])
def place_order(action, symbol, quantity=1):
    try:
        alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')
        if action == 'BUY':
            alpaca_client.submit_order(
                symbol='BTC/USD',
                qty=1,
                side='buy',
                time_in_force='cls'
            )
            return {"status": "buy order placed"}
        elif action == 'SELL':
            alpaca_client.submit_order(
                symbol='BTC/USD',
                qty=1,
                side='sell',
                time_in_force='cls'
            )
            return {"status": "sell order placed"}
        else:
            return {"error": "Invalid action"}
    except Exception as e:
        return {"status": "failed", "reason": str(e)}

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    action = data.get("action")
    symbol = data.get("symbol")
    quantity = data.get("quantity", 1)

    print(f"Received webhook request: action={action}, symbol={symbol}, quantity={quantity}")

    response = place_order(action, symbol, quantity)
    print(f"Alpaca API response: {response}")

    return jsonify(response)

    if action == 'BUY':
        place_order('BUY', symbol)
    elif action == 'SELL':
        place_order('SELL', symbol)
    else:
        return jsonify({"error": "Invalid action"}), 400

    return jsonify({"status": "success"}), 200

@app.route('/')
def home():
    return "Trading Bot is live!"

if __name__ == "__main__":
    print("Testing Alpaca order...")
    result = place_order("BUY", "NQ1!", 1)  # Test order for AAPL
    print("Order result:", result)
    app.run(host="0.0.0.0", port=10000)
