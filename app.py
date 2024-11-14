from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi

app = Flask(__name__)

API_KEY = 'PKCAXN5MUDCWCEK7XYC0'
API_SECRET = 'iexDDqoWlg10LhFDfjx7ZaRxXOMlboPVgmLTOpeL'
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
            profit_target = 100
            stop_loss_limit = 50
            
            order = api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc',
                order_class='bracket',
                take_profit={'limit_price': None}
                stop_loss={'stop_price': None}
            )

            filled_order = api.get_order(order.id)
            while filled_order.status != 'filled':
                filled_order = api.get_order(buy_order.id)

            buy_price = float(filled_order.filled_avg_price)
            print(f"Buy price: ${buy_price:.2f}")

            take_profit_price = buy_price + profit_target
            stop_loss_price = buy_price - stop_loss_limit

            order.take_profit['limit_price'] = take_profit_price
            order.stop_loss['stop_price'] = stop_loss_price
            
            print(f"Take Profit set at ${take_profit_price:.2f}")
            print(f"Stop Loss set at ${stop_loss_price:.2f}")
            
            return jsonify({
                "status": "buy order placed with take profit and stop loss",
                "order_id": order.id,
                "buy_price": buy_price,
                "take_profit_price": take_profit_price,
                "stop_loss_price": stop_loss_price
            })
            
        else:
            return jsonify({"status": "no action taken", "reason": "invalid action"}), 400
            
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
