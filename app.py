from flask import Flask, request, jsonify
import os
from alpaca_trade_api.rest import REST

app = Flask(__name__)

API_KEY = "PK3URU8NDWKD8FEMOFRS"
API_SECRET = "llEfnkpnYl27gHKlN2AJYmqcBkPyxmz2vckkhvvT"

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.content_type == 'application/json':
        data = request.get_json()
    elif request.content_type == 'text/plain':
        import json
        data = json.loads(request.data)
    else:
        return jsonify({"error": "Unsupported Content-Type"}), 415
        
    action = data.get("action")
    symbol = data.get("symbol", "BTC/USD")
    quantity = data.get("quantity", 1)

    print(f"Received webhook request: action={action}, symbol={symbol}, quantity={quantity}")

    response = place_order(action, symbol, quantity)
    print(f"Alpaca API response: {response}")

    return jsonify(response)

def place_order(action, symbol, quantity=1):
    try:
        alpaca_client = REST(API_KEY, API_SECRET, base_url='https://paper-api.alpaca.markets')
        
        if action == 'BUY':
            order = alpaca_client.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            return {"status": "buy order placed"}
        else:
            return {"status": "failed", "reason": "Invalid action"}
    
    except Exception as e:
        return {"status": "failed", "reason": str(e)}
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
