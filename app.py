from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi

app = Flask(__name__)

API_KEY = 'PK4GWFVXQQL2EUKIRZ0B'
API_SECRET = '5K3Ougjm7L0cs3fZBWKyltydFdZ7OjZqS3gU3U1V'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def place_order():
    try:
        data = request.json
        action = data.get('action')
        symbol = data.get('symbol')
        
        if action == 'BUY':
            quantity = 0.5
            profit_target = 20
            stop_loss_limit = 10

            last_trade = api.get_latest_trade(symbol)
            current_price = last_trade.price

            take_profit_price = buy_price + profit_target
            stop_loss_price = buy_price - stop_loss_limit
            
            order = api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc',
                order_class='bracket',
                take_profit={'limit_price': take_profit_price},
                stop_loss={'stop_price': stop_loss_price}
            )
            
            return jsonify({
                "status": "success",
                "order_id": order.id,
                "buy_price": current_price,
                "take_profit_price": take_profit_price,
                "stop_loss_price": stop_loss_price
            })
        else:
            return jsonify({"status": "error", "message": "Invalid action provided."}), 400
            
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
