# test_backtester.py

from backtester.core.data_handler import DataHandler
from backtester.strategies.test_strategy import TestStrategy
from backtester import run_backtest
from backtester.utils import performance, visualization

def main():
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-01-01"

    print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
    data = DataHandler().from_yahoo(ticker, start=start_date, end=end_date)

    print("Running backtest with TestStrategy...")
    results, broker = run_backtest(TestStrategy, data, return_broker=True)

    # Show final equity and summary
    final_equity = results["final_equity"]
    print(f"\nFinal Equity: ${final_equity:.2f}")
    print(f"Total Trades: {len(results['trade_log'])}")

    # Compute performance metrics
    equity_curve = results["equity_curve"]
    trade_log = results["trade_log"]
    print(broker.get_closed_trades())

    sharpe = performance.compute_sharpe_ratio(equity_curve)
    max_dd = performance.compute_max_drawdown(equity_curve)
    total_return = performance.compute_total_return(equity_curve)
    win_rate = performance.compute_win_rate(trade_log)

    print(f"\nPerformance Metrics:")
    print(f"  - Sharpe Ratio: {sharpe:.4f}")
    print(f"  - Max Drawdown: {max_dd:.2%}")
    print(f"  - Total Return: {total_return:.2%}")
    print(f"  - Win Rate: {win_rate:.2%}")

    # Plot equity curve against Buy & Hold
    buy_hold = [equity_curve[0] * (p / data['Close'].iloc[0]) for p in data['Close'].iloc[:len(equity_curve)]]
    visualization.plot_equity_curve(results["timestamps"], equity_curve, buy_hold)

    # Plot candlestick chart with trades
    visualization.plot_candles_with_trades(data, trade_log, timestamps=results["timestamps"])



if __name__ == "__main__":
    main()