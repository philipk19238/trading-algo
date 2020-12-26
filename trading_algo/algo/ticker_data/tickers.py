import pathlib 
import pandas as pd
import os

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()

BLACKLIST = set([
      "YOLO", "TOS", "CEO", "CFO", "CTO", "DD", "BTFD", "WSB", "OK", "RH",
      "KYS", "FD", "TYS", "US", "USA", "IT", "ATH", "RIP", "BMW", "GDP",
      "OTM", "ATM", "ITM", "IMO", "LOL", "DOJ", "BE", "PR", "PC", "ICE",
      "TYS", "ISIS", "PRAY", "PT", "FBI", "SEC", "GOD", "NOT", "POS", "COD",
      "AYYMD", "FOMO", "TL;DR", "EDIT", "STILL", "LGMA", "WTF", "RAW", "PM",
      "LMAO", "LMFAO", "ROFL", "EZ", "RED", "BEZOS", "TICK", "IS", "DOW"
      "AM", "PM", "LPT", "GOAT", "FL", "CA", "IL", "PDFUA", "MACD", "HQ",
      "OP", "DJIA", "PS", "AH", "TL", "DR", "JAN", "FEB", "JUL", "AUG",
      "SEP", "SEPT", "OCT", "NOV", "DEC", "FDA", "IV", "ER", "IPO", "RISE"
      "IPA", "URL", "MILF", "BUT", "SSN", "FIFA", "USD", "CPU", "AT",
      "GG", "ELON", "ROPE", "FDS", "ON", "CS", "U", "SJW", "MAGA", "NYC"
   ])

class TickerService:

    @staticmethod
    def get_ticker_df():
        for filename in os.listdir(CURRENT_DIRECTORY):
            if filename.startswith('nasdaq_screener') and filename.endswith('.csv'):
                filename = f'{CURRENT_DIRECTORY}/{filename}'
                return pd.read_csv(filename)

    @staticmethod 
    def get_ticker_set():
        ticker_set = set()
        ticker_csv = TickerService.get_ticker_df()
        for ticker in ticker_csv.Symbol:
            if ticker in BLACKLIST:
                continue
            ticker_set.add(ticker)
        return ticker_set
        
tickers = TickerService.get_ticker_set()

