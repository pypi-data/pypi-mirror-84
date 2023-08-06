import lightgbm as lgb
from pandas import DataFrame, DateOffset, concat
from datetime import datetime
from joblib import dump, load
from stories.model_list.base import rmse, make_stationary, invert_forecast, define_diff

def prepare_forecast_LIGHTGBM(train, test, columns, folder=None, settings=None):
    X_train = create_features(train, columns, True)
    X_test = create_features(test, columns, True)

    series = concat([train[columns['forecast']], test[columns['forecast']]])

    cfg_list = configs(settings, series)
    scores = []
    for cfg in cfg_list:
        prediction, model, error = train_LIGHTGBM(X_train, X_test, cfg, train, test, columns)
        scores.append((cfg, error))
        best_score = cfg
    
    if len(scores) > 1:
        scores = [r for r in scores if r[1] != None]
        scores.sort(key=lambda tup: tup[1])
        best_score = scores[0][0]
        prediction, model, error = train_LIGHTGBM(X_train, X_test, best_score, train, test, columns)

    iterations, learning_rates, depths, diff = best_score
    if folder is not None:
        dump(model, folder + 'LIGHTGBM.save')
    return (prediction, model, {'iterations': iterations, 'learning_rates': learning_rates, 'depths': depths, 'diff': diff}, [])

def future_forecast_LIGHTGBM(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    if df_forecast is None:
        if columns['date_type'] == 'D':
            df_forecast = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(days=x+1) for x in range(steps)]
        elif columns['date_type'] == 'W':
            df_forecast = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(weeks=x+1) for x in range(steps)]
        elif columns['date_type'] == 'M':
            df_forecast = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(months=x+1) for x in range(steps)]
        future_features = create_features(df_forecast, columns, False)
    else:
        future_features = create_features(df_forecast, columns, True)
    
    
    if folder is not None:
        model = load(folder + 'LIGHTGBM.save')
    prediction = model.predict(future_features)
    prediction = invert_forecast(df[columns['forecast']], prediction, best_config['diff'])
    return prediction, []

def create_features(data, columns, case):
    if case:
        if columns['features']:
            df = data.loc[:, data.columns != columns['forecast']]
        else:
            df = DataFrame({'date': data.index}, index=data.index)
            case = False
    else:
        df = DataFrame({'date': data}, index=data)
    df['month'] = df.index.month
    df['year'] = df.index.year
    if columns['date_type'] == 'D' or columns['date_type'] == 'W':
        df['week'] = df.index.week
    if not case:
        del df['date']
    return df

def train_LIGHTGBM(X_train, X_test, config, train, test, columns):
    num_iterations, learning_rates, max_depths, order = config

    series_diff = make_stationary(concat([train[columns['forecast']], test[columns['forecast']]]), order)
    y_train = series_diff[:(len(series_diff)-len(test[columns['forecast']]))]
    y_test = series_diff[-len(test[columns['forecast']]):]
    if order == 1:
        X_train = X_train[1:]
    elif order == 2:
        X_train = X_train[2:]

    d_train = lgb.Dataset(X_train, y_train)
    d_test = lgb.Dataset(X_test, y_test)
    params = {
        'objective' : 'regression',
        'num_iterations': num_iterations,
        'learning_rate': learning_rates,
        'max_depth': max_depths
    }

    model_fit = lgb.train(
        params,
        d_train,
        valid_sets=[d_train, d_test],
        valid_names=['train', 'test']
    )

    prediction = model_fit.predict(X_test)
    prediction = invert_forecast(train[columns['forecast']], prediction, order)
    error = rmse(y_test.values.flatten(), prediction)
    return (prediction, model_fit, error)

def configs(settings, series):
    models = []
    if settings is None:
        iterations = [100]
        learning_rates = [0.1]
        depths = [-1]
        diffs = [define_diff(series)]
    else:
        iterations = [100] if 'default' in settings['LIGHTGBM']['iterations'] else settings['LIGHTGBM']['iterations']
        learning_rates = [0.1] if 'default' in settings['LIGHTGBM']['learning_rates'] else settings['LIGHTGBM']['learning_rates']
        depths = [-1] if 'default' in settings['LIGHTGBM']['depths'] else settings['LIGHTGBM']['depths']
        diffs = [define_diff(series)] if 'default' in settings['XGBOOST']['diff'] else settings['XGBOOST']['diff']
    
    for iteration in iterations:
        for learning_rate in learning_rates:
            for depth in depths:
                for diff in diffs:
                    cfg = [iteration, learning_rate, depth, diff]
                    models.append(cfg)

    return models