import pandas as pd
import yfinance as yf
from nsepy import get_history
from datetime import date

ticker = yf.Ticker("^NSEI").history(period="5y",interval = "1d")

nifty_tri = get_history(
    symbol="NIFTY 50",
    start=date(2019,1,1),
    end=date(2024,12,31),
    index=True,
    return_type="TOTAL_RETURN"
)

print(nifty_tri.head())
