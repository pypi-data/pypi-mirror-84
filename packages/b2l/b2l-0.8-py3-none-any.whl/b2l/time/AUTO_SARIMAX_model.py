from pmdarima.arima import auto_arima
# from pmdarima.arima import auto_arima, AutoARIMA
# from pmdarima.pipeline import Pipeline
# from pmdarima.preprocessing import BoxCoxEndogTransformer, FourierFeaturizer
from joblib import dump, load
from datetime import datetime
from pandas import DateOffset, Series
from sklearn.preprocessing import StandardScaler

def prepare_forecast_AUTO_SARIMAX(train, test, columns, folder=None, settings=None):
    if columns['features']:
        exog_train = train.loc[:, train.columns != columns['forecast']]
        exog_test = test.loc[:, test.columns != columns['forecast']]
        scaler = StandardScaler()
        scaler = scaler.fit(exog_train.values)
        exog_train = scaler.transform(exog_train.values)
        exog_test = scaler.transform(exog_test.values)
        dump(scaler, folder + 'SARIMAX_AUTO_scaler.save')
    else:
        exog_train = None
        exog_test = None

    train, test = train[columns['forecast']].values.flatten(), test[columns['forecast']].values.flatten()
    m = {'M': 12, 'D': 7, 'W': 52, 'Y': 1, 'Q': 4}[columns['date_type']]
    model = auto_arima(train, exogenous=exog_train, m=m, trend='c', seasonal=True, trace=True, error_action='ignore', suppress_warnings=True, stepwise=True, max_p=5, max_q=5, max_P=5, max_Q=5)
    params = model.get_params()
    # best_score = [params['order'], params['seasonal_order'], params['trend']]
    [(p,d,q), (P,D,Q,m), t] = [params['order'], params['seasonal_order'], params['trend']]
    if folder is not None:
        dump(model, folder + 'AUTO_SARIMAX.save')
    prediction = model.predict(n_periods=len(test), exogenous=exog_test)
    return (prediction, model, {'p': p, 'd': d, 'q': q, 'P': P, 'D': D, 'Q': Q, 'm': m, 't': t}, [])

def future_forecast_AUTO_SARIMAX(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    if folder is not None:
        model = load(folder + 'AUTO_SARIMAX.save')

    if df_forecast is None:
        exog = None

        max_date = datetime.strptime(max_date, '%Y-%m-%d')
        if columns['date_type'] == 'D':
            test_period = Series([max_date - DateOffset(days=x+1) for x in range(365)])
        elif columns['date_type'] == 'W':
            test_period = Series([max_date - DateOffset(weeks=x+1) for x in range(52)])
        elif columns['date_type'] == 'M':
            test_period = Series([max_date - DateOffset(months=x+1) for x in range(12)])
        test_period = test_period[test_period.dt.year == max_date.year]
        test_period = len(test_period) + 1
        if (columns['date_type'] == 'D' and test_period < 365) or (columns['date_type'] == 'W' and test_period < 52) or (columns['date_type'] == 'M' and test_period < 12):
            period = test_period
        else:
            period = 0
            
        prediction = model.predict(n_periods=period+steps, exogenous=exog)
        prediction = prediction[-steps:]
    else:
        scaler = load(folder + 'SARIMAX_AUTO_scaler.save')
        exog = scaler.transform(df_forecast.values)
        prediction = model.predict(n_periods=len(df_forecast.index), exogenous=exog)

    return prediction, []
