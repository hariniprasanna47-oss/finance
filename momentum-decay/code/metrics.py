import pandas as pd
from .utils import window

def cum_returns(df,t, offset_val,lbw_bool):
    start,end = window(timestamp=t,offset_dict=offset_val,lbw = lbw_bool)
    #df = df.set_index("Date")
    lbw_prices = df.loc[start:end,:]
    returns = lbw_prices.pct_change()

    cumulative_returns = (1 + returns).cumprod().iloc[-1].to_frame("cumulative_returns")
    cumulative_returns = cumulative_returns.reset_index(names='ticker')
    print("Cumulative returns calculation done.")

    output_path = "../outputs/tables/cumulative_returns_" + str(offset_val["months"]) + "mo.csv"
    cumulative_returns.to_csv(output_path,index=False)
    return cumulative_returns

def portfolio(df):
    sorted_values = df.sort_values("cumulative_returns")
    #top and bottom 10% of the portfolio
    num_values = int(round(sorted_values.shape[0] * 0.10))
    portfolio = pd.concat([sorted_values.head(num_values),sorted_values.tail(num_values)])
    return portfolio