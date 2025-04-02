# backtester/core/strategy.py
# Author: Krittin Hirunchupong

'''
strategy.py
    This module is a blueprint for all the strategy that can be implemented.
'''

from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    def __init__(self, data: pd.DataFrame, broker):
        self.data = data
        self.broker = broker
        self.current_index = 0 # This is the current index of the current bar in the DataFrame

    '''
    set_index()
    This method sets the current row index that the strategy is operating on.
    This is called on every bar by the backtest engine.
    '''
    def set_index(self, idx: int):
        self.current_index = idx

    '''
    get_price()
    This method returns the current price for a specific column at the current index.
    '''
    def get_price(self, column: str = 'Close') -> float:
        return self.data.iloc[self.current_index][column]
    
    '''
    get_lookback()
    This method returns a slice of the last 'window' number of price values (inclusive)
    This method is useful for calculating indicators like moving averages, RSI, etc.
    '''
    def get_lookback(self, column: str = 'Close', window: int = 10) -> pd.Series:
        start = max(0, self.current_index - window + 1)
        return self.data.iloc[start:self.current_index + 1][column]
        
    
    '''
    on_data()
    This is an abstract method that must be implemented by every strategy.
    This method is called by the backtest engine at every step.
    '''
    @abstractmethod
    def on_data(self, timestamp=None):
        pass

    def close_all_trades(self, timestamp=None):
        self.broker.close_all_trades(price=self.get_price(), timestamp=timestamp)