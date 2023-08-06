
from statsmodels.tsa.ar_model import AutoReg
from pandas import concat
from joblib import dump, load
from base import rmse

def prepare_forecast_AR(train, test, columns, folder=None, settings=None):
    series = concat([train[columns['forecast']], test[columns['forecast']]])
    cfg_list = configs(settings)
    scores = []
    for cfg in cfg_list:
        prediction, model, error = train_AR(series, cfg, train, test, columns)
        scores.append((cfg, error))
        best_score = cfg
    
    if len(scores) > 1:
        scores = [r for r in scores if r[1] != None]
        scores.sort(key=lambda tup: tup[1])
        best_score = scores[0][0]
        prediction, model, error = train_AR(series, best_score, train, test, columns)

    lag, trend, seasonal = best_score
    if folder is not None:
        dump(model, folder + 'AR.save')
    
    return (prediction, model, {'lags': lag, 'trend': trend, 'seasonal': seasonal}, [])

def future_forecast_AR(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    if folder is not None:
        model = load(folder + 'AR.save')
    prediction = model.predict(len(df), len(df) + steps - 1)
    return prediction.values, []

def train_AR(series, config, train, test, columns):
    lag, trend, seasonal = config
    model = AutoReg(series, lags=lag, trend=trend, seasonal=seasonal)
    model_fit = model.fit()
    prediction = model_fit.predict(len(series) - len(test), len(series) - 1)

    error = rmse(test.values.flatten(), prediction)
    return (prediction, model_fit, error)

def configs(settings):
    models = []

    if settings is None:
        lags = [1,2,3,4,5]
        trends = ['c']
        seasonals = [True, False]
    else:
        lags = [1,2,3,4,5] if 'default' in settings['AR']['lags'] else settings['AR']['lags']
        trends = ['c'] if 'default' in settings['AR']['trend'] else settings['AR']['trend']
        seasonals = [True, False] if 'default' in settings['AR']['seasonal'] else settings['AR']['seasonal']

    for lag in lags:
        for trend in trends:
            for seasonal in seasonals:
                cfg = [lag, trend, seasonal]
                models.append(cfg)

    return models