import pandas as pd
from langchain.tools import tool
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller

import numpy as np

@tool
def calculate_hurst_exponent(ts):
    """
    Calculate the Hurst exponent of a time series.


    Parameters:
    ts (list): A list representing the time series data.

    Returns:
    float: The Hurst exponent of the time series. Returns NaN if the time series is too short 
           or if the computation fails.
    """

    ts = np.log(np.cumsum(ts))

    lags = range(2, 100)
    tau = []

    for lag in lags:
        if len(ts) <= lag:
            break

        lagged_diff = ts[lag:] - ts[:-lag]
        if len(lagged_diff) > 1:
            tau.append(np.std(lagged_diff))

    tau = np.array(tau)

    # Filter out invalid (zero or NaN) tau values
    valid = (tau > 0)
    lags = np.array(lags[:len(tau)])[valid]
    tau = tau[valid]

    if len(tau) < 2:
        return np.nan

    # Perform linear regression on log-log scale
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0



