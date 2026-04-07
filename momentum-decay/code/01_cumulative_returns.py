import yfinance as yf
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

# Reading the .csv from NSE website
try:
    nsei_table = pd.read_csv("../data/ind_nifty50list.csv")
    tickers = nsei_table['Symbol'].dropna().str.strip().tolist()
    tickers = [t + ".NS" for t in tickers]
    print(f"Total tickers after removing NA's = {len(tickers)}")
except Exception as e:
    print(f"Failed to read data/ind_nifty50list.csv {e}")

# TO DO: Add period, tickers as parameter.
prices = pd.DataFrame()
try:
    data = yf.download(tickers, period="1y", auto_adjust=True)
    prices = data["Close"]
except Exception as e:
    print(f"yFinance download failed : {e}")

if not prices.empty:
    print(f"Total stocks with data: {len(prices.columns)}")
else:
    print("prices empty")

# Visualization:
plt.figure(figsize=(20, 6))
sns.heatmap(prices.isna(), 
            cbar=False, 
            yticklabels=False,
            cmap=["steelblue", "salmon"],
            xticklabels=True,
            linewidths=0.5,
            linecolor="white")
plt.xticks(rotation=45, ha="right", fontsize=6)
plt.legend(handles=[
    mpatches.Patch(color="steelblue", label="Available"),
    mpatches.Patch(color="salmon", label="Missing")
],fontsize=8, handleheight=0.8, handlelength=1, bbox_to_anchor=(1.05, 1), loc="upper left")
plt.title("Missing data across NIFTY 50")
plt.savefig('../data/isNA_heatmap.png')

# Checking if all data is present for time period required of the data:
# Assuming a threshold window
threshold = 3
index = (prices.isna().rolling(threshold).sum() == threshold).any()
if index.any():
    print(f"The following tickers will be excluded from downstream analysis due to missing data: {prices.columns[index].tolist()}")
    prices = prices.drop(columns=prices.columns[index])
    print(f"Number of column in data: {prices.shape[1]}")

# Data imputation, ffill and keep moving. 
# else drop the ticker.
prices = prices.ffill()
prices.to_csv("../data/cleaned_nifty50_1y.csv")

#returns
returns = prices.pct_change()
cumulative_returns = returns.sum()


#What to do if that fails
#2. Add lookback window as parameter
#1. check if all the tickers have information for the lookback window.
#2. survivorship bias acknowledgement
#3. iterate lookback windows and save files at every point. with correct names