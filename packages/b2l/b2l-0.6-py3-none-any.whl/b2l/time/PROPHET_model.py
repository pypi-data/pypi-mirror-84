from fbprophet import Prophet
from joblib import dump, load
from pandas import concat
from stories.model_list.base import rmse

def prepare_forecast_PROPHET(train, test, columns, folder=None, settings=None):
    train = train.reset_index()
    test = test.reset_index()
    train = train.rename(columns={columns['date']: 'ds', columns['forecast']: 'y'})
    test = test.rename(columns={columns['date']: 'ds', columns['forecast']: 'y'})
    series = concat([train, test])
    cfg_list = configs(columns['date_type'], settings)
    scores = []
    for cfg in cfg_list:
        predictions, model = train_PROPHET(series, columns, cfg)
        predictions = predictions[-len(test):]
        error = rmse(test['y'].values.flatten(), predictions)
        scores.append((cfg, error))
        best_score = cfg

    if len(scores) > 1:
        scores = [r for r in scores if r[1] != None]
        scores.sort(key=lambda tup: tup[1])
        best_score = scores[0][0]
        predictions, model = train_PROPHET(series, columns, best_score)
        predictions = predictions[-len(test):]
    
    if columns['features']:
        baseline = forecast_baseline_PROPHET(model, series, columns, len(test))
        baseline = baseline.values
    else:
        baseline = []

    order_yearly, order_weekly = best_score
    model.stan_backend.logger = None
    if folder is not None:
        dump(model, folder + 'PROPHET.save')
    return (predictions.values, model, {'order_yearly': order_yearly, 'order_weekly': order_weekly}, baseline)

def forecast_baseline_PROPHET(model, series, columns, test_len):
    freq = {'M': 'MS', 'D': 'D', 'W': 'W', 'Y': 'Y', 'Q': 'Q'}[columns['date_type']]

    forecast_period_promo = model.make_future_dataframe(periods=0, freq=freq)
    for column in series.columns:
        if column not in ['ds', 'y']:
            forecast_period_promo[column] = series[column].values
    prediction_promo = model.predict(forecast_period_promo)
    prediction_promo = prediction_promo['yhat']

    forecast_period_baseline = model.make_future_dataframe(periods=0, freq=freq)
    for column in series.columns:
        if column not in ['ds', 'y']:
            forecast_period_baseline[column] = 0
    prediction_baseline = model.predict(forecast_period_baseline)
    prediction_baseline = prediction_baseline['yhat']

    baseline_train = (series['y'].values)[:-test_len] + (prediction_promo[:-test_len] - prediction_baseline[:-test_len])
    baseline_test = prediction_promo[-test_len:] - (prediction_baseline[-test_len:] - prediction_promo[-test_len:])

    baseline = concat([baseline_train, baseline_test])
    return baseline

def future_forecast_PROPHET(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    if folder is not None:
        model = load(folder + 'PROPHET.save')
    freq = {'M': 'MS', 'D': 'D', 'W': 'W', 'Y': 'Y', 'Q': 'Q'}[columns['date_type']]
    if df_forecast is not None:
        steps = len(df_forecast)
        df_forecast = concat([df, df_forecast])
        df_forecast = df_forecast.reset_index()
    forecast_period = model.make_future_dataframe(periods=steps, freq=freq)

    if df_forecast is not None:
        for feature in df_forecast.columns:
            forecast_period[feature] = df_forecast.loc[-len(forecast_period):, feature]
    
    forecast = model.predict(forecast_period)
    forecast = forecast['yhat']
    forecast = forecast[-steps:]

    if df_forecast is not None:
        for column in forecast_period:
            if column != 'ds':
                forecast_period[column] = 0
        baseline = model.predict(forecast_period)
        baseline = baseline['yhat']
        baseline = baseline[-steps:]
        baseline = forecast - (baseline - forecast)
        baseline = baseline.values
    else:
        baseline = []

    return forecast.values, baseline

def train_PROPHET(series, columns, config):
    freq = {'M': 'MS', 'D': 'D', 'W': 'W', 'Y': 'Y', 'Q': 'Q'}[columns['date_type']]
    y_cfg, w_cfg = config
    model = Prophet()
    if columns['date_type'] in ['M', 'W', 'Y', 'Q']:
        model.add_seasonality(name='yearly', period=365.25, fourier_order=y_cfg, mode='additive')
    else:
        model.add_seasonality(name='yearly', period=365.25, fourier_order=y_cfg, mode='additive')
        model.add_seasonality(name='weekly', period=52, fourier_order=w_cfg, mode='additive')

    if columns['features']:
        for column in series.columns:
            if column not in ['ds', 'y']:
                model.add_regressor(column)
    model_fit = model.fit(series)
    forecast_period = model_fit.make_future_dataframe(periods=0, freq=freq)
    if columns['features']:
        for column in series.columns:
            if column not in ['ds', 'y']:
                forecast_period[column] = series[column].values
    prediction = model_fit.predict(forecast_period)
    prediction = prediction['yhat']
    return (prediction, model_fit)

def configs(date_type, settings):
    models = []
    if settings is None:
        order_years = [10]
        order_weeks = [3]
    else:
        order_years = [10] if 'default' in settings['PROPHET']['order_yearly'] else settings['PROPHET']['order_yearly']
        
        # if date_type in ['M', 'W', 'Y', 'Q']:
        order_weeks = [3] if 'default' in settings['PROPHET']['order_weekly'] else settings['PROPHET']['order_weekly']
        # else:
        #     order_weeks = [3] if 'default' in settings['PROPHET']['order_weekly'] else settings['PROPHET']['order_weekly']
        #     order_weeks = [None]
    
    for order_year in order_years:
        for order_week in order_weeks:
            cfg = [order_year, order_week]
            models.append(cfg)
	
    return models