from math import sqrt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
from statsmodels.tsa.stattools import adfuller
from collections import Counter

# root mean square error
def rmse(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))
# mean square error
def mse(actual, predicted):
    return mean_squared_error(actual, predicted)
# mean absolute percentage error
def mape(actual, predicted): 
    actual, predicted = np.array(actual), np.array(predicted)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    mape = 0 if mape == np.inf or mape == -np.inf else mape
    return mape

def correct_class(actual, predicted): 
    array = []
    for key, value in enumerate(predicted):
        if value == actual[key]:
            array.append(True)
        else:
            array.append(False)
    count = Counter(array)
    return count[False]/(count[True]+count[False])

# mean absolute error
def mae(actual, predicted):
    return mean_absolute_error(actual, predicted)
# Mean Forecast Error (or Forecast Bias)
def bias(actual, predicted):
    actual, predicted = np.array(actual), np.array(predicted)
    return np.mean(actual - predicted)

# split a univariate dataset into train/test sets
# def train_test_split(data, ratio = 0.75):
#     train_size = int(len(data) * ratio)
#     test_size = int(len(data)) - train_size
#     return data[:train_size], data[train_size:]
def train_test_split(df, date_type):
    periods_number = {'D': 365, 'W': 51, 'M': 12}[date_type]

    max_year = (df.index.year).max()
    test = df[df.index.year == max_year]

    min_year = (df.index.year).min()
    first_year_length = len(df[df.index.year == min_year])
    if first_year_length < periods_number:
        train = df[(df.index.year < max_year) & (df.index.year > min_year)]
    else:
        train = df[df.index.year < max_year]

    return train, test

def make_stationary(series, order):
    if order == 0:
        return series
    elif order == 1:
        return series.diff().dropna()
    elif order == 2:
        return (series.diff().dropna()).diff().dropna()

def define_diff(series):
    r = adfuller(series, autolag='AIC')
    if r[1] <= 0.05:
        # Data is Stationary
        return 0
    else:
        # Data is NOT Stationary
        series_diff1 = series.diff().dropna()
        r = adfuller(series_diff1, autolag='AIC')
        if r[1] <= 0.05:
            # Data is Stationary
            return 1
        else:
            # Data is NOT Stationary
            series_diff2 = series_diff1.diff().dropna()
            r = adfuller(series_diff2, autolag='AIC')
            if r[1] <= 0.05:
                # Data is Stationary
                return 2
            else:
                # Can't make stationary
                return 0

def invert_forecast(train, forecast, order):
    # Revert back the differencing to get the forecast to original scale
    if order == 0:
        return forecast
    elif order == 1:
        return (train.values)[-1] + forecast.cumsum(axis=0)
    elif order == 2:
        return ((train.values)[-1]-(train.values)[-2]) + forecast.cumsum(axis=0)