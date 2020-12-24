import os 
import pandas as pd 

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
      "GG", "ELON", "ROPE"
   ])

class TickerService:

    @staticmethod
    def get_ticker_df():
        for filename in os.listdir(os.getcwd()):
            if filename.startswith('nasdaq_screener') and filename.endswith('.csv'):
                return pd.read_csv(filename)

    @staticmethod 
    def get_ticker_dict():
        ticker_dict = {}
        ticker_csv = TickerService.get_ticker_df()
        assert ticker_csv
        for ticker, name in zip(ticker_csv.Symbol, ticker_csv.Name):
            if ticker in BLACKLIST:
                continue
            name = name.split()[0]
            ticker_dict[ticker.lower()] = ticker
            ticker_dict[name.lower()] = ticker
        return ticker_dict
        
tickers = TickerService.get_ticker_dict()

