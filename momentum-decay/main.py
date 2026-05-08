import pandas as pd
import numpy as np
import code.data as cd
import code.metrics as cm

### scope and time line definition
timestamp = "2025-06-16"
lookbacks = [{"months":1},{"months":3},{"months":6},{"months":12}]
lookforward = [{"weeks":1},{"months":1},{"months":3},{"months":6}]

tickers = cd.clean_tickers("../data/ind_nifty50list.csv")
#Prices calculated for the maximum period of 18 months
prices = cd.download_data(tickers = tickers,time_period = timestamp)
clean_prices = cd.clean_data(prices=prices)
cum_returns = cm.cum_returns(df = clean_prices,t = timestamp, offset_val = {"months":1},lbw_bool = True)
portfolio = cm.portfolio(df=cum_returns)
print(portfolio)
#TO-DO: Make all the timestamp, df and whatever [parameter uniform]