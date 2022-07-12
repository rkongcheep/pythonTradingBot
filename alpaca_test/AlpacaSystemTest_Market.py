'''
Try getting Historical data
'''

api_key = 'PK42O6ZKJXD0E21ND9F9'
api_secret = 'Uxo3MG5E1cRovH2MMNXj0kKJSDFq9gszSk8c4hfV'
base_url = 'https://data.alpaca.markets/v1beta1/crypto'#'https://paper-api.alpaca.markets'

from alpaca_trade_api.rest import REST, TimeFrame

api = REST(api_key, api_secret, base_url, api_version='v2')

AAPL_price = api.get_crypto_bars('BTCUSD',TimeFrame.Minute,'2022-04-29','2022-04-29').df
#AAPL_quote = api.get_crypto_quotes("ETHUSD", "2021-06-08", "2021-06-08", limit=10).df

(AAPL_price.to_csv('BTCUSDDD.csv'))
