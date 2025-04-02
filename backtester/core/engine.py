# backtester/core/engine.py
# Author: Krittin Hirunchupong

'''
engine.py
    This module constructs an engine in order to execute the backtest.
    Can be executed by just calling run() after initializing an engine object. 
'''


class BacktestEngine:
    """
    The main loop that runs a strategy on historical data.
    """

    def __init__(self, strategy_class, data, broker, **strategy_kwargs):
        self.data = data
        self.broker = broker
        self.strategy = strategy_class(data, broker, **strategy_kwargs)

        self.equity_curve = []  # Portfolio value over time
        self.pnl_curve = []     # PnL (unrealized) over time
        self.timestamps = []    # Timestamps for plotting
        self.start_index = None
        self.end_index = None


    def run(self):
        for i in range(len(self.data)):
            self.strategy.set_index(i)

            price = self.data.iloc[i]['Close']
            timestamp = self.data.index[i]

            self.broker.update_price(price)
            self.strategy.on_data(timestamp=timestamp)

            if self.start_index is None:
                self.start_index = i
            self.end_index = i

            self.timestamps.append(timestamp)
            self.equity_curve.append(self.broker.get_equity())
            self.pnl_curve.append(self.broker.get_open_position_summary()['unrealized_pnl'])


    def get_results(self):
        return {
            'timestamps': self.timestamps,
            'equity_curve': self.equity_curve,
            'pnl_curve': self.pnl_curve,
            'final_equity': self.equity_curve[-1] if self.equity_curve else self.broker.cash,
            'trade_log': self.broker.get_trade_log()
        }
