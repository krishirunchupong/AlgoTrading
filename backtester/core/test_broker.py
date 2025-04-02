import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backtester.core.broker import Broker

broker = Broker(initial_cash=10_000)
broker.update_price(100)

id1 = broker.execute_order(qty=1, side='buy')
id2 = broker.execute_order(qty=1, side='sell')

print("Open trades:", broker.get_open_trades())

broker.update_price(110)
broker.close_trade(trade_id=id1)

print("Remaining open trades:", broker.get_open_trades())
print("Closed Trades:", broker.get_closed_trades())
print("Final equity:", broker.get_equity())

