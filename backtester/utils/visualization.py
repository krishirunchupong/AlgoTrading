# backtester/utils/visualization.py
# Author: Krittin Hirunchupong

'''
visualization.py
    This module contains all the method regarding visualizing the strategy.
    Visualization Included:
        - Equity Curve
        - Candle Stick chart with trade overlays
'''


import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import numpy as np

def plot_equity_curve(timestamps, strategy_equity, buy_hold_equity):
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, strategy_equity, label="Strategy Equity", linewidth=2)
    plt.plot(timestamps, buy_hold_equity, label="Buy & Hold Equity", linestyle="--", color="gray")
    
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.title("Equity Curve Comparison")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_candles_with_trades(data, trades, timestamps=None):
    df = data.copy()
    df.index.name = 'Date'

    if timestamps is not None:
        start = timestamps[0]
        end = timestamps[-1]
        df = df.loc[start:end]

    buy_signals = pd.Series(index=df.index, dtype=float)
    sell_signals = pd.Series(index=df.index, dtype=float)

    for trade in trades:
        ts = trade.get("timestamp")
        if ts not in df.index:
            continue

        if trade.get("status") == "open":
            if trade["side"] == "buy":
                buy_signals[ts] = df.loc[ts]["Low"] * 0.98
            elif trade["side"] == "sell":
                sell_signals[ts] = df.loc[ts]["High"] * 1.02
        elif trade.get("status") == "closed":
            if trade["exit_side"] == "sell":
                sell_signals[ts] = df.loc[ts]["High"] * 1.02
            elif trade["exit_side"] == "buy":
                buy_signals[ts] = df.loc[ts]["Low"] * 0.98

    apds = [
        mpf.make_addplot(buy_signals, type='scatter', marker='^', color='green', markersize=100),
        mpf.make_addplot(sell_signals, type='scatter', marker='v', color='red', markersize=100)
    ]


    mpf.plot(df, type='candle', style='yahoo', addplot=apds, volume=True,
             title="Candlestick Chart with Trades", xlim=(df.index[0], df.index[-1]))
