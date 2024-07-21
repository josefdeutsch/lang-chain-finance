import numpy as np
from arch.unitroot import ADF

def calculate_optimal_hedge_ratio(ts1, ts2):
    """
    Calculate the optimal hedge ratio and perform the CADF test on the residuals.

    Parameters:
    ts1 (list): List containing the first time series data.
    ts2 (list): List containing the second time series data.

    Returns:
    tuple: A tuple containing the optimal hedge ratio (beta) and the results of the CADF test on the residuals.
    """
    
    # Convert lists to numpy arrays
    ts1 = np.array(ts1)
    ts2 = np.array(ts2)
    
    # Ensure both time series have the same length
    min_length = min(len(ts1), len(ts2))
    ts1 = ts1[:min_length]
    ts2 = ts2[:min_length]
    
    # Calculate optimal hedge ratio "beta" using polyfit
    beta_hr, intercept = np.polyfit(ts1, ts2, 1)
    
    # Calculate residuals
    residuals = ts2 - (beta_hr * ts1 + intercept)
    
    # Perform ADF test on the residuals
    adf_test = ADF(residuals)
    cadf = (adf_test.stat, adf_test.pvalue, adf_test.lags, adf_test.nobs, adf_test.critical_values)

    return beta_hr, cadf

# Example usage with provided data
if __name__ == "__main__":
    
    ts1 = [70773.64, 69394, 69304.05, 69649.9, 69497.73, 67316.53, 68248.6, 66756.5, 66004.39, 66192, 66481.81, 65152.8, 64943.79, 64841.46, 64087.9, 64235.01, 63171.43, 64253, 60815.1, 61615.39, 60313.35, 60860, 62668.26, 62830.13, 62039.45, 56639.43, 58244.75, 55854.09, 57230.64, 57230.64, 55649.8, 57230.64] 
    ts2 = [3812.09, 3676.69, 3680.84, 3706.26, 3665.86, 3497.31, 3559.14, 3467.65, 3479.53, 3566.69, 3622.1, 3509.81, 3482.06, 3559.14, 3510.73, 3517.19, 3494.09, 3418.42, 3350.59, 3393.6, 3369.31, 3445.58, 3373.62, 3373.26, 3432.37, 3438.36, 3416.17, 3291.74, 3058.89, 2981.74, 3067.39, 2930.78]

    # Calculate ADF test results
    beta_hr, adf_results = calculate_optimal_hedge_ratio(ts1, ts2)
    
    # Print the results of the ADF test
    print("Optimal Hedge Ratio (Beta):", beta_hr)
    print("ADF Test Results:")
    print("ADF Statistic:", adf_results[0])
    print("p-value:", adf_results[1])
    print("Lags Used:", adf_results[2])
    print("Number of Observations Used:", adf_results[3])
    print("Critical Values:")
    for key, value in adf_results[4].items():
        print(f"\t{key}: {value}")

    print(len(ts1), len(ts2))
