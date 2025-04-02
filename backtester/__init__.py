# backtester/__init__.py

from backtester.core.broker import Broker
from backtester.core.engine import BacktestEngine

def run_backtest(strategy_class, data, initial_cash=100_000, commission=0.001, return_broker=False, **strategy_kwargs):
    broker = Broker(initial_cash=initial_cash, commission=commission)
    engine = BacktestEngine(strategy_class, data, broker, **strategy_kwargs)
    engine.run()
    results = engine.get_results()

    if return_broker:
        return results, broker
    return results