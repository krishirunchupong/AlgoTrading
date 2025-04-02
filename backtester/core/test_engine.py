
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pandas as pd
from backtester.core.broker import Broker
from backtester.core.engine import BacktestEngine
from backtester.core.strategy import Strategy
from backtester.core.data_handler import DataHandler
from backtester.strategies.sma_crossover import SmaCrossover
from backtester.strategies.mean_reversion import MeanReversion
from backtester.utils.performance import (
    compute_sharpe_ratio,
    compute_max_drawdown,
    compute_total_return,
    compute_win_rate
)
from backtester.utils.visualization import *

class TestStrategy(Strategy):
    def on_data(self, timestamp=None):
        price = self.get_price()

        if self.current_index == 1:
            self.broker.execute_order(qty=1, side='buy', price=price, timestamp= timestamp)

        elif self.current_index == 3:
            open_ids = list(self.broker.open_trades.keys())
            if open_ids:
                self.broker.close_trade(trade_id=open_ids[0], price=price, timestamp=timestamp)

loader = DataHandler()
df = loader.from_yahoo('UNG', start='2023-01-01', end='2023-02-01', interval='1d')

broker = Broker(initial_cash=100_000)
#engine = BacktestEngine(SmaCrossover, df, broker, short_window=100, long_window=200)
engine = BacktestEngine(MeanReversion, df, broker, window=70, threshold=0.02)

engine.run()
results = engine.get_results()
initial_price = df.loc[results['timestamps'][0]]['Close']
buy_hold_equity = [broker.initial_cash * (price / initial_price) for price in df.loc[results['timestamps']]['Close']]


# Print results
print("\n📈 BACKTEST SUMMARY")
print(f"Final Equity: ${results['final_equity']:.2f}")
print("Trade Log:")
for trade in results['trade_log']:
    print(trade)

print(broker.get_open_trades())

sharpe = compute_sharpe_ratio(results['equity_curve'])
drawdown = compute_max_drawdown(results['equity_curve'])
total_return = compute_total_return(results['equity_curve'])
win_rate = compute_win_rate(results['trade_log'])

print("\n📊 PERFORMANCE METRICS")
print(f"Total Return: {total_return:.2%}")
print(f"Sharpe Ratio: {sharpe:.3f}")
print(f"Max Drawdown: {drawdown:.2%}")
print(f"Win Rate: {win_rate:.2%}")
print(f"Final Equity: ${results['final_equity']:,.2f}")
print(f"Total Trades: {len(results['trade_log'])}")

plot_equity_curve(results['timestamps'], results['equity_curve'], buy_hold_equity)
plot_candles_with_trades(df, results["trade_log"], timestamps=results["timestamps"])