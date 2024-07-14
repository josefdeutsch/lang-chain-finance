import pandas as pd
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller
from langchain.tools import tool
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller
import numpy as np

@tool
def calculate_optimal_hedge_ratio(ts1: str, ts2: str):

    """
    Calculate the optimal hedge ratio and perform the CADF test on the residuals.

    Parameters:
    df (pd.DataFrame): DataFrame containing the time series data.
    ts1 (str): Column name of the first time series in the DataFrame.
    ts2 (str): Column name of the second time series in the DataFrame.

    Returns:
    tuple: A tuple containing the optimal hedge ratio (beta) and the results of the CADF test on the residuals.
    """
    
    # Build a data frame
    df = pd.DataFrame()
    
    # Calculate optimal hedge ratio "beta"
    res = OLS(df[ts2], df[ts1]).fit()
    beta_hr = res.params[0]

    # Calculate the residuals of the linear combination
    df["res"] = df[ts2] - beta_hr * df[ts1]

    # Calculate and output the CADF test on the residuals
    cadf = adfuller(df["res"])

    return beta_hr, cadf



import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tsa.stattools import adfuller

@tool
def calculate_optimal_hedge_ratio2(ts1: list, ts2: list):
    """
    Calculate the optimal hedge ratio and perform the CADF test on the residuals.

    Parameters:
    ts1 (list): List containing the first time series data.
    ts2 (list): List containing the second time series data.

    Returns:
    tuple: A tuple containing the optimal hedge ratio (beta) and the results of the CADF test on the residuals.
    """
    
    # Convert the lists to numpy arrays
    ts1 = np.array(ts1)
    ts2 = np.array(ts2)
    
    # Ensure the time series have the same length by trimming the longer series
    min_length = min(len(ts1), len(ts2))
    ts1 = ts1[:min_length]
    ts2 = ts2[:min_length]
    
    # Reshape ts1 for regression
    ts1 = ts1.reshape(-1, 1)
    
    # Calculate optimal hedge ratio "beta"
    res = OLS(ts2, ts1).fit()
    beta_hr = res.params[0]

    # Calculate the residuals of the linear combination
    residuals = ts2 - beta_hr * ts1.flatten()

    # Calculate and output the CADF test on the residuals
    cadf = adfuller(residuals)

    return beta_hr, cadf


