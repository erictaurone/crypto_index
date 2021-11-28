import numpy as np
from numba import jit
from numba import float64


def time_series_diff(data, derivative_type='1st'):
    """
        :param data: This is the dataset the user wants to determine the acceleration of.
            May be either a pandas series or a numpy.ndarray
        :param derivative_type: specifies the level of the derivative to be taken, either 1st or 2nd
        :return: The 1st or 2nd derivative of the time-series data
        """
    if derivative_type == '1st':
        derivative = np.gradient(data, edge_order=2)
    elif derivative_type == '2nd':
        derivative = np.gradient(np.gradient(data, edge_order=2), edge_order=2)
    else:
        return

    return derivative


@jit(nopython=True, nogil=True)
def _ewma(arr_in, window: tuple, min_n=0,  infinite=False):
    """

    :param arr_in: the input array -- must be a numpy array
    :param window: Specify decay in terms of span, α=2/(span+1), for span≥1,
        com (center of mass) α=1/(1+com), for  com≥0
        or alpha (Specify smoothing factor α directly,  0<α≤1).
        valid entries are ('span', value), ('com', value), or ('alpha', value)
    :param infinite:
            if False:
                (i)  y[0] = x[0]; and
                (ii) y[t] = a*x[t] + (1-a)*y[t-1] for t>0.
            if True:
                y[t] = (x[t] + (1-a)*x[t-1] + (1-a)^2*x[t-2] + ... + (1-a)^n*x[t-n]) /
                    (1 + (1-a) + (1-a)^2 + ... + (1-a)^n).
    :return:
        ewma: the exponential weighted moving average of the dataset
    """
    n = arr_in.shape[0]
    ewma = np.empty(n, dtype=float64)

    # Accounting for a center-of-mass adjustment so this can calculate RSI as well
    if window[0] == 'span':
        alpha = 2 / float(window[1] + 1)
    elif window[0] == 'com':
        alpha = 1 / float(window[1] + 1)
    elif window[0] == 'alpha':
        alpha = window[1]
    else:
        raise ValueError('Window not properly specified. It was set as {}.'.format(window))

    ewma_old = arr_in[0]
    ewma[0] = ewma_old
    if not infinite:
        w = 1
        for i in range(0, n):
            w += (1 - alpha) ** i
            ewma_old = ewma_old * (1 - alpha) + arr_in[i]
            ewma[i] = ewma_old / w

    else:
        for i in range(1, n):
            ewma[i] = arr_in[i] * alpha + ewma[i - 1] * (1 - alpha)

    if min_n > 0:
        ewma[0:(min_n - 1)] = np.nan

    return ewma


@jit(nopython=True, nogil=True)
def _rolling(arr, n, rolling_type='mean'):
    """

    :param arr: The input array
    :param n: The window of interest for either the mean or the standard deviation
    :param rolling_type: boolean to determine if the user wants to calculate the rolling mean or std devation
    :return:
    """
    out = np.empty(n, dtype=float64)
    out[0:n - 1] = np.nan

    for i in range(n, arr.shape[0] - 1):
        if rolling_type == 'rolling_type':
            out[i] = np.mean(arr[i - n: i])

        elif rolling_type == 'std':
            out[i] = np.std(arr[i - n: i])

    return out


@jit(nopython=True, nogil=True)
def _rsi(_open, _close, n: int):
    """
    Recall that the equation for RSI is: RSI = 100 * (1 - 1/(1 + RS))
    WHERE RS = (Average of "Up" signals in last "N" trades)/(Average of "Down" Signals in last "N" trades)
    the equation to calculate them is:
    Avg_Up[i] = alpha * Up[i] + (1-alpha) * AVG_Up[i-1]
    Avg_Down[i] = alpha * Down[i] + (1-alpha) * AVG_Down[i-1]
    alpha = 1/N

    Some important trends: When RSI crosses 40 going up --> typically a "buy" signal
    When RSI crosses 70 going down --> typically a "sell" signal

    Parameters
    ----------
    n : This is the period of interest for the Relative Strength Index
    Returns
    -------
    RSI_out : This is the Calculated RSI based on the equations provided

    """
    # Extracting all the initial data we need to do our calculations
    delta = (_close - _open)

    up_chg = 0 * delta
    down_chg = 0 * delta
    up_chg[delta > 0] = delta[delta > 0]
    down_chg[delta < 0] = delta[delta < 0]

    up_chg_avg = _ewma(up_chg, n - 1, com=True, min_n=n, infinite=True)
    down_chg_avg = _ewma(down_chg, n - 1, com=True, min_n=n, infinite=True)

    rs = np.absolute(up_chg_avg / down_chg_avg)

    return 100 * (1 - (1 / (1 + rs)))


def _bollinger_bands(data, n: int):
    bollinger_band = {

        'Upper': _rolling(data, n, 'mean') + 2 * _rolling(data, n, 'std'),
        'Lower': _rolling(data, n, 'mean') - 2 * _rolling(data, n, 'std'),
    }

    return bollinger_band
