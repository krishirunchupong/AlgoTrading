# backtester/strategies/sma_crossover.py
# Author: Krittin Hirunchupong

'''
sma_crossover.py
    This is a very simple trading strategy that is used to test out the backtester. 
    Strategy:
        - Enters a long position when the short_sma crosses upward over the long_sma, and close all the short position
        - Enters a short position when the short_sma corsses downward over the long_sma, and close all the long position
'''

from backtester.core.strategy import Strategy

class SmaCrossover(Strategy):
    def __init__(self, data, broker, short_window=10, long_window=20):
        super().__init__(data, broker)
        self.short_window = short_window
        self.long_window = long_window

    def on_data(self, timestamp=None):
        if self.current_index < self.long_window:
            return
        
        short_ma = self.get_lookback('Close', self.short_window).mean()
        long_ma = self.get_lookback('Close', self.long_window).mean()
        price = self.get_price()
        open_ids = list(self.broker.open_trades.keys())

        if short_ma > long_ma:
            if open_ids:
                for trade_id in open_ids:
                    self.broker.close_trade(trade_id, price=price, timestamp=timestamp)
            self.broker.execute_order(qty=1, side='buy', price=price, timestamp=timestamp)

        elif short_ma < long_ma:
            if open_ids:
                for trade_id in open_ids:
                    self.broker.close_trade(trade_id, price=price, timestamp=timestamp)
            self.broker.execute_order(qty=1, side='sell', price=price, timestamp=timestamp)

        if self.current_index == len(self.data) - 1:
            self.close_all_trades(timestamp)

        