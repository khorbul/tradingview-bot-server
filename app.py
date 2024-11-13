from flask import Flask, request, jsonify
import json
from alpaca_trade_api.rest import REST

app = Flask(__name__)

API_KEY = "PK3URU8NDWKD8FEMOFRS"
API_SECRET = "llEfnkpnYl27gHKlN2AJYmqcBkPyxmz2vckkhvvT"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = json.loads(request.data.decode('utf-8'))

        print(f"Received webhook request with data: {data}")
        
        action = data.get("action")
        symbol = data.get("symbol", "BTC/USD")
        quantity = data.get("quantity", 1)

        print(f"Extracted action={action}, symbol={symbol}, quantity={quantity}")

        response = place_order(action, symbol, quantity)
        print(f"Order response: {response}")

        return jsonify(response)
        
    except json.JSONDecodeError:
        print("Failed to decode JSON")
        return jsonify({"error": "Invalid JSON format"}), 400


def place_order(action, symbol, quantity=1):
    try:
        alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')
        
        if action == 'BUY':
            print("Placing BUY order...")
            order = alpaca_client.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print("BUY order placed successfully.")
            return {"status": "buy order placed"}
        else:
            print("Invalid action received.")
            return {"status": "failed", "reason": "Invalid action"}
    
    except Exception as e:
        print(f"Error in place_order: {str(e)}")
        return {"status": "failed", "reason": str(e)}
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
