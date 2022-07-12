'''
System testing for getting account balance and Historical Data
'''


import alpaca_trade_api as tradeapi
import requests
from alpaca_trade_api.rest import REST, TimeFrame


# authentication and connection details
api_key = 'PK42O6ZKJXD0E21ND9F9'
api_secret = 'Uxo3MG5E1cRovH2MMNXj0kKJSDFq9gszSk8c4hfV'
base_url = 'https://paper-api.alpaca.markets'

# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()

### WIll try to send/get orders during market open later

def print_account_info():
    print('\n ************************ \n')
    print('ACCOUNT INFO'.center(24))
    print('\n ************************ \n')
    print(account)
    print('\n ************************ \n')
    return


def submit_market_order(order):
    api.submit_order(
        symbol=order['symbol'],
        qty=order['quantity'],  
        side=order['side'],
        type=order['type'],
        time_in_force=order['time_in_force'],
    )
    print(f'Submitting order: \nSide: {order["side"]}\tSymbol: {order["symbol"]}\tQuantity: {order["quantity"]}')
    pass

if __name__ == '__main__':
    print_account_info()
    order = {
        'symbol' : 'BTCUSD',
        'quantity': 0.003,
        'side':'buy',
        'type':'market',
        'time_in_force':'day'
    }
    submit_market_order(order)


   



