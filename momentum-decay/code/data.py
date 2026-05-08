import pandas as pd
import yfinance as yf
from .utils import window

def clean_tickers(file_path):
    try:
        nsei_table = pd.read_csv(file_path)
        tickers = nsei_table['Symbol'].dropna().str.strip().tolist()
        tickers = [t + ".NS" for t in tickers]
        print(f"Total tickers after removing NA's = {len(tickers)}")
    except Exception as e:
        print(f"Failed to read data/ind_nifty50list.csv {e}")
    return tickers

def download_data(tickers,time_period):
    prices = pd.DataFrame()
    t = pd.Timestamp(time_period)
    start_date = t - pd.DateOffset(months=12)
    end_date = t + pd.DateOffset(months=6)
    try:
        data = yf.download(tickers, auto_adjust = True, start = start_date, end = end_date)
        prices = data["Close"]
    except Exception as e:
        print(f"yFinance download failed : {e}")

    if not prices.empty:
        print(f"Total stocks with data: {len(prices.columns)}")
    else:
        print("prices empty")
    prices.to_csv("../data/raw_nifty50.csv")
    return prices

def clean_data(prices):
    threshold = 3
    index = (prices.isna().rolling(threshold).sum() == threshold).any()
    if index.any():
        print(f"The following tickers will be excluded from downstream analysis due to missing data: {prices.columns[index].tolist()}")
        prices = prices.drop(columns=prices.columns[index])
        print(f"Number of column in data: {prices.shape[1]}")
    clean_prices = prices.ffill()
    clean_prices.to_csv("../data/cleaned_nifty50.csv")
    return clean_prices