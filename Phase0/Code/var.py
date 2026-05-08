import numpy as np
import pandas as pd
import yfinance as yf


def get_returns(ticker, period):
    stock_data = yf.download(ticker, period=period)
    returns = stock_data["Close"].pct_change().dropna().squeeze()
    return returns

def historical_var_calc(returns, alpha):
    var_calc = returns.quantile((1 - alpha))
    return -var_calc

def sanity_check(window,returns,alpha):
    for i in window:
        var = returns.tail(i).quantile((1 - alpha))
        print(f"Sanity Check - VaR in window {i} days at {alpha * 100:.0f}% confidence level: {var * 100:.4f}%")

def num_of_values(window,alpha):
    print(f"Number of values in the {window} days at confidence interval {alpha * 100:.0f}%: {int(window * (1 - alpha))}")

def main():
    alpha = 0.95
    returns = get_returns("AAPL", "5y")
    window = [252,500]
    var = historical_var_calc(returns, alpha)
    print(f"Value at Risk (VaR) as per Historical Method at {alpha * 100:.0f}% confidence level: {var * 100:.4f}")
    sanity_check(window,returns,alpha)
    [num_of_values(w,alpha) for w in window]


if __name__ == "__main__":
    main()

# Add exception and error handling later yahoo download; maybe command line or yaml file for input
# plotting the returns distribution and the VaR threshold later
# Add rolling windows correctly later