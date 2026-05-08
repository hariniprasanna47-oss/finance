import yfinance as yf
import numpy as np
import pandas as pd
import time
from scipy.stats import norm

def get_returns(ticker, period, retries=3, backoff=1.0):
    """Download adjusted close prices and return percent changes.
    Retries the download on failure and raises clear errors for empty/malformed data.
    """
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            stock_data = yf.download(ticker, period=period, auto_adjust=True)
            break
        except Exception as e:
            last_exc = e
            if attempt == retries:
                raise RuntimeError(f"Failed to download data for {ticker} after {retries} attempts: {e}") from e
            time.sleep(backoff * attempt)

    if stock_data is None or getattr(stock_data, "empty", False):
        raise ValueError(f"No data downloaded for {ticker} with period={period}")

    if "Close" not in stock_data.columns:
        raise ValueError(f"'Close' column missing in downloaded data for {ticker}")

    # compute log returns
    returns = np.log(stock_data["Close"]).diff().dropna().squeeze()
    if getattr(returns, "empty", False):
        raise ValueError(f"No returns computed for {ticker} (insufficient data)")
    return returns

def get_parameters(returns):
    mean = returns.mean()
    stddev = returns.std()
    return mean, stddev

def calc_parametric_var(mean, stddev, alpha,time_horizon):
    z_score = norm.ppf(1 - alpha)
    var = -(z_score * stddev * (time_horizon ** 0.5)) 
    return var

def monetary_var(var, principal):
    return var * principal

def main():
    ticker = "AAPL"
    period = "5y"
    ci = 0.95
    returns = get_returns(ticker, period)
    mean, stddev = get_parameters(returns)
    parametric_var = calc_parametric_var(mean, stddev, ci, time_horizon=1)
    print(f"Mean: {mean:.6f}, Std Dev: {stddev:.6f}")
    print(f"Parametric VaR at {ci * 100:.0f}% confidence level: {parametric_var * 100:.4f}%")
    principal = 1000000  # Example principal amount
    monetary_loss = monetary_var(parametric_var, principal)
    print(f"Monetary VaR for principal ${principal}: ${monetary_loss:.2f}")

if __name__ == "__main__":
    main()

#plotting the returns distribution and the VaR threshold later
# normality test for returns distribution later
# returns.index.freq or infer frequency
# add the mean term back in the formula later; currently assuming mean is zero for simplicity