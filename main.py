

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

from strategy.deployer import StrategyDeployer
from strategy.basicstrat import strategy1,MovingAverageStrategy

def open_CONFIG():
    with open('CONFIG.json') as f:
        CONFIG = json.load(f)
    return CONFIG

def consumer_thread(CONFIG,strategy):
    global conn
    conn = Stream(CONFIG['KEYS']['api_key'],
                CONFIG['KEYS']['api_secret'],
                base_url = 'https://stream.data.alpaca.markets')

    StrDep = StrategyDeployer(CONFIG,strategy)
    conn.subscribe_crypto_bars(StrDep.onMarketDataReceived,'BTCUSD')
    conn.run()

def run_connection():
    try:
        conn.run()
    except KeyboardInterrupt:
        print("Interrupted execution by User")
        conn.stop()
        exit(0)
    except Exception as e:
        print(f"Exception {e}")
        conn.stop()
        pass
    finally:
        print("Trying to re-establish connection")
        time.sleep(3)
        run_connection(conn)
    


if __name__=='__main__':
    
    CONFIG = open_CONFIG()

    logging.basicConfig(format='%(asctime)s  %(levelname)s %(message)s',
                        level=logging.INFO)
    pool = ThreadPoolExecutor(1)
    print('Starting')
    #pool.submit(consumer_thread(CONFIG,MovingAverageStrategy(5,25)))
    pool.submit(consumer_thread(CONFIG,MovingAverageStrategy(5,25)))

    while True:
        try:
            print('Starting')
            pool.submit(consumer_thread(CONFIG,MovingAverageStrategy(5,25)))
            time.sleep(20)
            # print('Stopping')
            # conn.stop()
            # time.sleep(20)

        
        except KeyboardInterrupt:
            print("Interrupted execution by User")
            conn.stop()
            exit(0)
        
        except Exception as e:
            print(f"Exception {e}")
            pass