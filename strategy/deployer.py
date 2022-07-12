
import pandas as pd
from strategy.basicstrat import DIRECTION
import alpaca_trade_api as tradeapi


class StrategyDeployer():
    def __init__(self,CONFIG,strat=None):
        self.list_position=[]
        self.list_cash=[]
        self.list_holdings = []
        self.list_total=[]

        self.long_signal=False
        self.position=0
        self.cash=1000
        self.total=0
        self.holdings=0

        self.market_data_count=0
        self.prev_price = None
        self.statistical_model = None
        self.historical_data = pd.DataFrame(columns=['Trade','Price','OpenClose','HighLow'])
        self.strategy = strat

        self.api = tradeapi.REST(CONFIG['KEYS']['api_key']
        ,CONFIG['KEYS']['api_secret']
        ,CONFIG['KEYS']['base_url_paper'])


    async def onMarketDataReceived(self,price_update):
        if price_update.exchange == 'CBSE':
            print(f'Update {price_update.close}')
            print(f'Total {self.total}')
            if self.strategy:
                self.strategy.fit(price_update)
                predicted_value = self.strategy.predict(price_update)
            else:
                predicted_value = DIRECTION.HOLD

            action = 'hold'
            if predicted_value==DIRECTION.BUY:
                action = 'buy'
            if predicted_value==DIRECTION.SELL:
                action = 'sell'
            self.buy_sell_or_hold_something(price_update,action)
        else:
            pass
        


    def buy_sell_or_hold_something(self,price_update,action):
        if action == 'buy':
            cash_needed = 0.0025 * price_update.close
            if self.cash - cash_needed >=0:
                print(str(price_update.close) +
                      " send buy order for 0.0025 shares price=%.2f" % (price_update.close))
                self.api.submit_order(
                                symbol='BTCUSD',
                                qty=0.0025,  # fractional shares
                                side='buy',
                                type='market',
                                time_in_force='day',
                            )
                self.position += 0.0025
                self.cash -= cash_needed
            else:
                print('buy impossible because not enough cash')


        if action == 'sell':
            position_allowed=0.0025
            if self.position-position_allowed>=-position_allowed:
                print(str(price_update.close)+
                      " send sell order for 0.0025 shares price=%.2f" % (price_update.close))
                self.api.submit_order(
                                    symbol='BTCUSD',
                                    qty=0.0025,  # fractional shares
                                    side='sell',
                                    type='market',
                                    time_in_force='day',
                                )
                    
                self.position -= position_allowed
                self.cash -= -position_allowed * price_update.close
            else:
                print('sell impossible because not enough position')

        self.holdings = self.position * price_update.close
        self.total = (self.holdings + self.cash)
        # print('%s total=%d, holding=%d, cash=%d' %
        #       (str(price_update['date']),self.total, self.holdings, self.cash))

        self.list_position.append(self.position)
        self.list_cash.append(self.cash)
        self.list_holdings.append(self.holdings)
        self.list_total.append(self.holdings+self.cash)