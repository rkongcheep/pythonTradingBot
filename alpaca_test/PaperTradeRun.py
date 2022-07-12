


import sys
import os
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import requests
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream

api_key = 'PK42O6ZKJXD0E21ND9F9'
api_secret = 'Uxo3MG5E1cRovH2MMNXj0kKJSDFq9gszSk8c4hfV'
base_url = 'https://paper-api.alpaca.markets'
feed = 'iex'

from TradingStrategy.SimpleTradingStrategy import strategy1

market_feed = Stream(api_key, api_secret, base_url,data_feed=feed, raw_data=True)

## First, try to read and print price data

