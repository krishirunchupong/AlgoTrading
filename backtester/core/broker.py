# backtester/core/broker.py
# Author: Krittin Hirunchupong

'''
broker.py
    This module acts like broker where trades from strategies can be executed.
    The user could simply call execute_order() to open a buy/sell trade and call close_order() to close a buy/sell trade
'''


class Broker:
    def __init__(self, initial_cash=100_000, commission=0.001):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.commission = commission
        self.current_price = None

        self.next_trade_id = 1
        self.open_trades = {}    
        self.trade_log = []

    def update_price(self, price: float):
        self.current_price = price

    def execute_order(self, qty=1, side='buy', price=None, timestamp=None):
        price = price or self.current_price
        cost = qty * price
        fee = cost * self.commission

        if side == 'buy':
            self.cash -= (cost + fee)
        elif side == 'sell':
            self.cash += (cost - fee)
        else:
            raise ValueError("Invalid order side")

        trade_id = self.next_trade_id
        self.next_trade_id += 1

        trade = {
            'trade_id': trade_id,
            'side': side,
            'qty': qty,
            'price': price,
            'timestamp': timestamp,
            'status': 'open'
        }

        self.open_trades[trade_id] = trade
        self.trade_log.append({**trade})  # Record opening trade

        return trade_id  # Return the ID for external tracking

    def close_trade(self, trade_id, price=None, timestamp=None):
        if trade_id not in self.open_trades:
            raise ValueError(f"No open trade with ID {trade_id}")

        price = price or self.current_price
        trade = self.open_trades[trade_id]
        qty = trade['qty']
        entry_price = trade['price']
        side = trade['side']
        direction = 1 if side == 'buy' else -1

        # Execute reverse order to close
        exit_side = 'sell' if side == 'buy' else 'buy'
        exit_cost = qty * price
        fee = exit_cost * self.commission

        if exit_side == 'buy':
            self.cash -= (exit_cost + fee)
        else:
            self.cash += (exit_cost - fee)

        pnl = (price - entry_price) * qty * direction

        closed_trade = {
            'trade_id': trade_id,
            'entry_price': entry_price,
            'exit_price': price,
            'qty': qty,
            'entry_side': side,
            'exit_side': exit_side,
            'timestamp': timestamp,
            'pnl': pnl,
            'status': 'closed'
        }

        self.trade_log.append(closed_trade)
        del self.open_trades[trade_id]

    def close_all_trades(self, price=None, timestamp=None):
        for trade_id in list(self.open_trades.keys()):
            self.close_trade(trade_id, price=price, timestamp=timestamp)

    def get_open_position_summary(self):
        unrealized_pnl = 0
        net_position = 0
        for trade in self.open_trades.values():
            direction = 1 if trade['side'] == 'buy' else -1
            entry = trade['price']
            qty = trade['qty']
            net_position += direction * qty
            unrealized_pnl += (self.current_price - entry) * qty * direction

        return {
            'net_position': net_position,
            'unrealized_pnl': unrealized_pnl,
            'open_trades': len(self.open_trades)
        }

    def get_equity(self):
        return self.cash + self.get_open_position_summary()['unrealized_pnl']

    def get_trade_log(self):
        return self.trade_log

    def get_open_trades(self) -> str:
        """
        Returns a formatted string of all open trades,
        with 'Open trades:' heading and indented trade lines.
        """
        if not self.open_trades:
            return "Open trades:\n\tNone"

        lines = ["Open trades:"]
        for trade_id, trade in self.open_trades.items():
            line = (
                f"\tTrade ID {trade_id}: "
                f"{trade['side'].upper()} {trade['qty']} @ {trade['price']} | "
                f"Timestamp: {trade.get('timestamp', 'N/A')}"
            )
            lines.append(line)

        return "\n".join(lines)
    
    def get_closed_trades(self) -> str:
        """
        Returns a formatted string of all closed trades,
        with 'Closed trades:' heading and indented trade lines including PnL.
        """
        closed_trades = [t for t in self.trade_log if t.get('status') == 'closed']

        if not closed_trades:
            return "Closed trades:\n\tNone"

        lines = ["Closed trades:"]
        for trade in closed_trades:
            line = (
                f"\tTrade ID {trade['trade_id']}: "
                f"{trade['entry_side'].upper()} {trade['qty']} @ {trade['entry_price']} → "
                f"{trade['exit_side'].upper()} @ {trade['exit_price']} | "
                f"PnL: {trade['pnl']:.2f} | "
                f"Timestamp: {trade.get('timestamp', 'N/A')}"
            )
            lines.append(line)

        return "\n".join(lines)



