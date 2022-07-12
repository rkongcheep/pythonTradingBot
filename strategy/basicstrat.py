



import math
import os
import random
import re
import sys
import pandas as pd
from abc import ABC
from collections import deque
from sklearn.linear_model import LogisticRegression
import numpy as np

class DIRECTION:
    BUY=1
    SELL=-1
    HOLD = 0

class base_strategy(ABC):
    def predict(self):
        pass
    def fit(self,price):
        pass

class strategy1(base_strategy):
    def __init__(self):
        super().__init__()
        self.counter=0
    
    def predict(self, price):
        print(f'Predicting on {price}')
        self.counter += 1
        if self.counter % 3 == 1:
            return DIRECTION.BUY
        elif self.counter % 3 == 2:
            return DIRECTION.SELL
        else:
            return DIRECTION.HOLD


class MovingAverageStrategy(base_strategy):
    def __init__(self,short_window,long_window):
        super().__init__()
        self.long_win=long_window
        self.short_win = short_window
        self.smavg = 0
        self.lmavg = 0
        self.buy = True
        self.prices = []
    
    def predict(self, price):
        self.prices.append(price.close)
        if len(self.prices) > self.long_win:
            self.prices.pop(0)
        self.lmavg = np.mean(self.prices)
        self.smavg = np.mean(self.prices[-self.short_win:])
        print(f'ShortMA = {self.smavg}, LongMA = {self.lmavg}, ({len(self.prices)})')
        if(self.smavg>self.lmavg and not self.buy):
            self.buy = True
            return DIRECTION.SELL
        if(self.smavg<self.lmavg and self.buy):
            self.buy = False
            return DIRECTION.BUY

