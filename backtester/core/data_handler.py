# backtester/core/strategy.py
# Author: Krittin Hirunchupong

'''
strategy.py
    This module handles the data handling. Whether the user decides to import a csv file or pull data directly from yfinance, 
    this module will clean the data to get it ready for further processing.
    
PLEASE NOTE: Yahoo has limits...
    - For 15m intervals, Yahoo only gives data for the past 60 days
    - For 1m intervals, Yahoo only gives data for the past 7 days
    - For Daily, Weekly, and Monthly it is around 20 years
'''

import pandas as pd
import yfinance as yf


class DataHandler:
    def __init__(self):
        pass

    def from_csv(self, file_path: str, datetime_col: str = 'Date') -> pd.DataFrame:
        df = pd.read_csv(file_path, parse_dates=[datetime_col])
        df.set_index(datetime_col, inplace=True)
        df = df.sort_index()
        df.columns = df.columns.str.title().str.replace(' ', '')
        df.columns = [col.replace('Adjclose', 'AdjClose') for col in df.columns]
        return df

    def from_yahoo(self, ticker: str, start: str, end: str, interval: str = '1d') -> pd.DataFrame:
        valid_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', 
                           '1h', '1d', '5d', '1wk', '1mo', '3mo']

        if interval not in valid_intervals:
            raise ValueError(f"Invalid interval '{interval}'. Must be one of: {valid_intervals}")

        df = yf.download(ticker, start=start, end=end, interval=interval, auto_adjust=False)
        df.dropna(inplace=True)

        # Flatten MultiIndex if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0].replace(' ', '') for col in df.columns]

        df.columns = [col.title().replace('Adjclose', 'AdjClose') for col in df.columns]
        df.index.name = 'Datetime'

        return df
