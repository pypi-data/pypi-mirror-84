from warnings import filterwarnings, catch_warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from b2l.base import rmse
from joblib import dump, load
from datetime import datetime
from pandas import DateOffset, Series
from pmdarima.arima import ndiffs, nsdiffs
from shutil import make_archive, unpack_archive
from os import remove
from sklearn.preprocessing import StandardScaler

def prepare_forecast_SARIMAX(train, test, columns, folder=None, settings=None):

    if columns['features']:
        exog_train = train.loc[:, train.columns != columns['forecast']]
        exog_test = test.loc[:, test.columns != columns['forecast']]

        exog_train_baseline = exog_train.copy()
        for column in exog_train_baseline.columns:
            exog_train_baseline[column] = 0
        exog_test_baseline = exog_test.copy()
        for column in exog_test_baseline.columns:
            exog_test_baseline[column] = 0

        scaler = StandardScaler()
        scaler = scaler.fit(exog_train.values)
        exog_train = scaler.transform(exog_train.values)
        exog_test = scaler.transform(exog_test.values)
        exog_train_baseline = scaler.transform(exog_train_baseline.values)
        exog_test_baseline = scaler.transform(exog_test_baseline.values)
        dump(scaler, folder + 'SARIMAX_scaler.save')
    else:
        exog_train = None
        exog_test = None

    train, test = train[columns['forecast']].values.flatten(), test[columns['forecast']].values.flatten()
    cfg_list = configs(columns['date_type'], train, settings)
    scores = []

    for cfg in cfg_list:
        error = None
        try:
            with catch_warnings():
                filterwarnings("ignore")
                predictions, model = train_SARIMAX(train, exog_train, exog_test, cfg, len(test))
                error = rmse(test, predictions)
        except:
            error = None

        if error is not None:
            print(' > Model[%s] %.3f' % (str(cfg), error))
            # print(model.aic)
        scores.append((cfg, error))
        best_score = cfg
    
    if len(scores) > 1:
        scores = [r for r in scores if r[1] != None]
        scores.sort(key=lambda tup: tup[1])
        best_score = scores[0][0]
        prediction, model = train_SARIMAX(train, exog_train, exog_test, best_score, len(test))
    
    # if columns['features']:
    #     forecast_baseline_SARIMAX(model, train, test, exog_train, exog_test, exog_train_baseline, exog_test_baseline)

    if folder is not None:
        model.save(folder + 'SARIMAX.save')
        make_archive(folder + 'SARIMAX', 'zip', folder, 'SARIMAX.save')
        remove(folder + 'SARIMAX.save')
    [(p,d,q), (P,D,Q,m)] = best_score
    return (prediction, model, {'p': p, 'd': d, 'q': q, 'P': P, 'D': D, 'Q': Q, 'm': m}, [])

def future_forecast_SARIMAX(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    if folder is not None:
        unpack_archive(folder + 'SARIMAX.zip', folder, 'zip')
        model = load(folder + 'SARIMAX.save')
        remove(folder + 'SARIMAX.save')

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

        prediction = model.forecast(steps=period+steps, exog=exog)
        prediction = prediction[-steps:]
    else:
        scaler = load(folder + 'SARIMAX_scaler.save')
        exog = scaler.transform(df_forecast.values)
        prediction = model.forecast(steps=len(df_forecast.index), exog=exog)

    return prediction, []

# def forecast_baseline_SARIMAX(model, train, test, exog_train, exog_test, exog_train_baseline, exog_test_baseline):

#     print('exog_train')
#     print(exog_train)
#     print('exog_train_baseline')
#     print(exog_train_baseline)
#     prediction_train_promo = model.predict(start=0, exog=exog_train)
#     prediction_train_baseline = model.predict(start=0, exog=exog_train_baseline)
#     # prediction_train_promo = model.forecast(steps=-len(train), exog=exog_train)
#     # prediction_train__baselone = model.forecast(steps=-len(train), exog=exog_train_baseline)
#     prediction_test_promo = model.forecast(steps=len(test), exog=exog_test)
#     prediction_test_baseline = model.forecast(steps=len(test), exog=exog_test_baseline)
#     print('train')
#     print(train)
#     print(len(train))
#     print('prediction_train_promo')
#     print(prediction_train_promo)
#     print(len(prediction_train_promo))
#     print('prediction_train_baseline')
#     print(prediction_train_baseline)
#     print(len(prediction_train_baseline))
#     print('prediction_train_promo-prediction_train_baseline')
#     print(prediction_train_promo-prediction_train_baseline)
#     print('prediction_test_promo')
#     print(prediction_test_promo)
#     print(len(prediction_test_promo))
#     print('prediction_test_baseline')
#     print(prediction_test_baseline)
#     print(len(prediction_test_baseline))
#     print('prediction_test_promo-prediction_test_baseline')
#     print(prediction_test_promo-prediction_test_baseline)
#     # return prediction

def train_SARIMAX(train, exog_train, exog_test, config, step):
    order, sorder = config
    model = SARIMAX(endog=train, exog=exog_train, order=order, seasonal_order=sorder, enforce_stationarity=False, enforce_invertibility=False)
    model_fit = model.fit(disp=False)
    prediction = model_fit.forecast(steps=step, exog=exog_test)
    return (prediction, model_fit)
 
def configs(date_type, train, settings):
    models = []

    m_params = {'M': [12], 'D': [365], 'W': [52], 'Y': [1], 'Q': [4]}[date_type]

    if settings is None:
        p_params = [0, 1, 2]
        d_params = [ndiffs(train, test='adf')]
        q_params = [0, 1, 2]
        q_params = [0, 1, 2]
        P_params = [0, 1, 2]
        try:
            D_params = [nsdiffs(train, m=m_params[0])]
        except Exception:
            D_params = [0, 1]
        Q_params = [0, 1, 2]
    else:
        p_params = [0, 1, 2] if 'default' in settings['SARIMAX']['p'] else settings['SARIMAX']['p']
        
        if 'default' in settings['SARIMAX']['d']:
            d_params = [ndiffs(train, test='adf')]
        elif 'adf'in settings['SARIMAX']['d'] or 'kpss' in settings['SARIMAX']['d'] or 'pp' in settings['SARIMAX']['d']:
            d_params = [ndiffs(train, test=settings['SARIMAX']['d'][0])]
        else:
            d_params = settings['SARIMAX']['d']

        q_params = [0, 1, 2] if 'default' in settings['SARIMAX']['q'] else settings['SARIMAX']['q']

        P_params = [0, 1, 2] if 'default' in settings['SARIMAX']['P'] else settings['SARIMAX']['P']

        if 'default' in settings['SARIMAX']['D'] or 'ch' in settings['SARIMAX']['D']:
            try:
                D_params = [nsdiffs(train, m=m_params[0])]
            except Exception:
                D_params = [0, 1]
        else:
            D_params = settings['SARIMAX']['D']

        Q_params = [0, 1, 2] if 'default' in settings['SARIMAX']['Q'] else settings['SARIMAX']['Q']


    # # t_params = ['n', 'c', 't', 'ct']
    # t_params = ['n', 'c']

    for p in p_params:
        for d in d_params:
            for q in q_params:
                for P in P_params:
                    for D in D_params:
                        for Q in Q_params:
                            for m in m_params:
                                # for t in t_params:
                                # cfg = [(p,d,q), (P,D,Q,m), t]
                                cfg = [(p,d,q), (P,D,Q,m)]
                                models.append(cfg)

    return models