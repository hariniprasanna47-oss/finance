import pandas as pd

def window(timestamp,offset_dict,lbw):
    t = pd.Timestamp(timestamp)
    if lbw:
        start = t - pd.DateOffset(**offset_dict)
        return str(start),str(t)
    else:
        start = t + pd.DateOffset(days=1)
        end = t +  pd.DateOffset(**offset_dict)
        return str(start),str(end)