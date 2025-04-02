# backtester/utils/performance.py
# Author: Krittin Hirunchupong 

'''
performance.py
    This module contains all the method that calculates the performance metrics of a strategy.
    Metrics Included:
        - Sharpe Ratio
        - Max Drawdown
        - Total Return
        - Win Rate
'''
import numpy as np

def compute_sharpe_ratio(equity_curve, risk_free_rate = 0.0, freq=252):
    returns = np.diff(equity_curve) / equity_curve[:-1]
    excess_returns = returns - (risk_free_rate / freq)
    if np.std(excess_returns) == 0:
        return 0
    sharpe = np.mean(excess_returns) / np.std(excess_returns)
    return sharpe * np.sqrt(freq)

def compute_max_drawdown(equity_curve):
    peak = np.maximum.accumulate(equity_curve)
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()

def compute_total_return(equity_curve):
    return (equity_curve[-1] / equity_curve[0]) - 1

def compute_win_rate(trade_log):
    wins = 0
    total = 0
    for trade in trade_log:
        if trade.get("status") == "closed":
            pnl = trade.get("pnl", 0)
            if pnl > 0:
                wins += 1
            total += 1
    return wins / total if total > 0 else 0