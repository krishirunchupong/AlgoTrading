from backtester.core.strategy import Strategy

class MeanReversion(Strategy):
    def __init__(self, data, broker, window=20, threshold=0.02, trailing_stop=0.05):
        super().__init__(data, broker)
        self.window = window
        self.threshold = threshold
        self.trailing_stop = trailing_stop
        self.trailing_prices = {}  # trade_id -> best_price_seen

    def on_data(self, timestamp=None):
        if self.current_index < self.window:
            return

        close = self.get_price('Close')
        ma = self.get_lookback('Close', self.window).mean()
        deviation = (close - ma) / ma
        open_ids = list(self.broker.open_trades.keys())

        # ➤ Trailing stop-loss check
        for tid in open_ids:
            trade = self.broker.open_trades.get(tid)
            if not trade:
                continue

            side = trade['side']

            # Initialize or update best price
            best = self.trailing_prices.get(tid, close)
            if side == 'buy':
                best = max(best, close)
                if close < best * (1 - self.trailing_stop):
                    self.broker.close_trade(tid, price=close, timestamp=timestamp)
                    self.trailing_prices.pop(tid, None)
                    continue
            elif side == 'sell':
                best = min(best, close)
                if close > best * (1 + self.trailing_stop):
                    self.broker.close_trade(tid, price=close, timestamp=timestamp)
                    self.trailing_prices.pop(tid, None)
                    continue

            # Save updated best price
            self.trailing_prices[tid] = best

        # ➤ Get current position (after potential stops)
        open_ids = list(self.broker.open_trades.keys())  # Refresh after possible stops
        current_pos = 0
        for tid in open_ids:
            trade = self.broker.open_trades.get(tid)
            if trade:
                current_pos += 1 if trade['side'] == 'buy' else -1

        # ➤ Mean reversion logic
        if deviation < -self.threshold and current_pos <= 0:
            for tid in open_ids:
                trade = self.broker.open_trades.get(tid)
                if trade and trade['side'] == 'sell':
                    self.broker.close_trade(tid, price=close, timestamp=timestamp)
                    self.trailing_prices.pop(tid, None)
            self.broker.execute_order(qty=1, side='buy', price=close, timestamp=timestamp)

        elif deviation > self.threshold and current_pos >= 0:
            for tid in open_ids:
                trade = self.broker.open_trades.get(tid)
                if trade and trade['side'] == 'buy':
                    self.broker.close_trade(tid, price=close, timestamp=timestamp)
                    self.trailing_prices.pop(tid, None)
            self.broker.execute_order(qty=1, side='sell', price=close, timestamp=timestamp)

        elif abs(deviation) < 0.005:
            self.close_all_trades(timestamp=timestamp)
            self.trailing_prices.clear()
