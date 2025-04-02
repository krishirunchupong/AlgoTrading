# backtester/strategies/test_strategy.py
from backtester.core.strategy import Strategy

class TestStrategy(Strategy):
    def __init__(self, data, broker):
        super().__init__(data, broker)
        self.holding_period = 10
        self.entry_interval = 5
        self.trades = []  # Stores (trade_id, entry_index)

    def on_data(self, timestamp=None):
        current_idx = self.current_index

        # Check if we should buy today
        if current_idx % self.entry_interval == 0:
            price = self.get_price()
            trade_id = self.broker.execute_order(qty=100, side='buy', price=price, timestamp=timestamp)
            self.trades.append((trade_id, current_idx))

        # Check if any position has reached the 10-day holding period
        trades_to_close = []
        for trade_id, entry_idx in self.trades:
            if current_idx - entry_idx >= self.holding_period:
                self.broker.close_trade(trade_id, price=self.get_price(), timestamp=timestamp)
                trades_to_close.append((trade_id, entry_idx))

        # Remove closed trades from the list
        self.trades = [t for t in self.trades if t not in trades_to_close]
