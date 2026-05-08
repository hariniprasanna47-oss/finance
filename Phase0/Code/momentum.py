import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download 5 years of data for a few Nifty 500 stocks
tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "TATAMOTORS.NS"]

data = yf.download(tickers, start="2019-01-01", end="2024-01-01")["Close"]

print(data.head(10))
print(data.shape)