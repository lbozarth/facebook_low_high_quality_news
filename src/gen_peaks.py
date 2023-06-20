import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from statsmodels.tsa.seasonal import seasonal_decompose


def outliers_iqr(ys):
    # use seasonal decomposition to remove trend and seasonality first
    # the Q3+1.5*IQR approach
    quartile_1, quartile_3 = np.percentile(ys, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    return np.where((ys > upper_bound) | (ys < lower_bound))


def outliers_iqr_v2(ys, iqr_thres_low, iqr_thres_high, distance=14):
    try:
        # the Q3+1.5*IQR approach
        quartile_1, quartile_3 = np.percentile(ys, [25, 75])
        iqr = quartile_3 - quartile_1
        lower_bound = quartile_3 + (iqr * iqr_thres_low)
        upper_bound = quartile_3 + (iqr * iqr_thres_high)
        height_range = (lower_bound, upper_bound)

        peaks, _ = find_peaks(ys, height=height_range, distance=distance)
        return peaks
    except ValueError as e:
        raise e


def get_peaks(ys0, freq, iqr_thres):
    # the ys0 is the oirginal time-eries
    # freq, weekly, biweekly?
    decomp_result = seasonal_decompose(ys0, model='additive', period=freq)  # weekly
    ys = decomp_result.resid
    ys = [0 if pd.isna(y) else y for y in ys]
    results = {}
    a_idce = outliers_iqr(ys)
    # a_idce = outliers_iqr_v2(ys, iqr_thres_low=iqr_thres[0], iqr_thres_high=iqr_thres[1])
    results['iqr'] = a_idce.tolist()
