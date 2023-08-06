
from statsmodels.tsa.arima_model import ARIMA
from pandas import concat
from joblib import dump, load
from stories.model_list.base import rmse

def prepare_forecast_MA(train, test, columns, folder=None, settings=None):
    series = concat([train[columns['forecast']], test[columns['forecast']]])
    prediction, model, error = train_MA(series, train, test, columns)
    if folder is not None:
        dump(model, folder + 'MA.save')
    return (prediction, model, {}, [])

def future_forecast_MA(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    if folder is not None:
        model = load(folder + 'MA.save')
    prediction = model.predict(len(df), len(df) + steps - 1)
    # print('prediction')
    # print(prediction)
    return prediction.values, []

def train_MA(series, train, test, columns):
    model = ARIMA(series, order=(0, 0, 2))
    model_fit = model.fit(disp=False)
    prediction = model_fit.predict(len(series) - len(test), len(series) - 1)
    # print('prediction')
    # print(prediction)
    error = rmse(test.values.flatten(), prediction)
    return (prediction, model_fit, error)