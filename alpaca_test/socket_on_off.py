

import logging
import threading
import asyncio
import time
import os
import json

from concurrent.futures import ThreadPoolExecutor

from debugpy import connect
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL


def open_CONFIG():
    with open('CONFIG.json') as f:
        CONFIG = json.load(f)
    return CONFIG

async def handle_trades(bar):
    print('trade',bar.close)

def consumer_thread(CONFIG):
    global conn
    conn = Stream(CONFIG['KEYS']['api_key'],
                CONFIG['KEYS']['api_secret'],
                base_url = 'https://stream.data.alpaca.markets')
    conn.subscribe_crypto_bars(handle_trades,'BTCUSD')
    conn.run()


if __name__=='__main__':
    
    os.chdir("..")
    CONFIG = open_CONFIG()
    print(CONFIG)

    logging.basicConfig(format='%(asctime)s  %(levelname)s %(message)s',
                        level=logging.INFO)
    pool = ThreadPoolExecutor(1)

    while True:
        try:
            print('Starting')
            pool.submit(consumer_thread(CONFIG))
            time.sleep(20)
            print('Stopping')
            conn.stop()
            time.sleep(20)
        
        except KeyboardInterrupt:
            print("Interrupted execution by User")
            conn.stop()
            exit(0)
        
        except Exception as e:
            print(f"Exception {e}")
            pass


    

