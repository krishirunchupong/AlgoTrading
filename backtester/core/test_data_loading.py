# test_data_loading.py (in root or examples folder)

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backtester.core.data_handler import DataHandler



loader = DataHandler()

# Get 15-minute bars for the last 30 days
df_15m = loader.from_yahoo('AAPL', start='2025-03-01', end='2025-03-26', interval='15m')
print(df_15m.head())


# # Load from CSV
# df_csv = loader.from_csv('data/aapl.csv')
# print(df_csv.head())
