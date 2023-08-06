from catboost import CatBoostClassifier, CatBoost, CatBoostRegressor
from pandas import DataFrame, DateOffset, concat
from datetime import datetime
from b2l.base import rmse, make_stationary, invert_forecast, define_diff

def prepare_forecast_CATBOOST(train, test, columns, folder=None, settings=None):
    X_train = create_features(train, columns, True)
    X_test = create_features(test, columns, True)

    series = concat([train[columns['forecast']], test[columns['forecast']]])

    cfg_list = configs(settings, series)
    scores = []
    for cfg in cfg_list:
        prediction, model, error = train_CATBOOST(X_train, X_test, cfg, train, test, columns, folder)
        scores.append((cfg, error))
        best_score = cfg
    
    if len(scores) > 1:
        scores = [r for r in scores if r[1] != None]
        scores.sort(key=lambda tup: tup[1])
        best_score = scores[0][0]
        prediction, model, error = train_CATBOOST(X_train, X_test, best_score, train, test, columns, folder)

    iterations, learning_rates, depths, diff = best_score
    if folder is not None:
        model.save_model(folder + 'CATBOOST', format='cbm')
    return (prediction, model, {'iterations': iterations, 'learning_rates': learning_rates, 'depths': depths, 'diff': diff}, [])

def future_forecast_CATBOOST(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
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
        model = CatBoost()
        model.load_model(folder + 'CATBOOST', format='cbm')
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

def train_CATBOOST(X_train, X_test, config, train, test, columns, folder):
    iterations, learning_rates, depths, order = config

    series_diff = make_stationary(concat([train[columns['forecast']], test[columns['forecast']]]), order)
    y_train = series_diff[:(len(series_diff)-len(test[columns['forecast']]))]
    y_test = series_diff[-len(test[columns['forecast']]):]
    if order == 1:
        X_train = X_train[1:]
    elif order == 2:
        X_train = X_train[2:]

    model = CatBoostRegressor(iterations=iterations, learning_rate=learning_rates, depth=depths, train_dir=folder + 'catboost_info')
    model_fit =  model.fit(X_train, y_train)
    prediction = model_fit.predict(X_test)
    prediction = invert_forecast(train[columns['forecast']], prediction, order)
    error = rmse(y_test.values.flatten(), prediction)
    return (prediction, model_fit, error)

def configs(settings, series):
    models = []
    if settings is None:
        iterations = [None]
        learning_rates = [None]
        depths = [None]
        diffs = [define_diff(series)]
    else:
        iterations = [None] if 'default' in settings['CATBOOST']['iterations'] else settings['CATBOOST']['iterations']
        learning_rates = [None] if 'default' in settings['CATBOOST']['learning_rates'] else settings['CATBOOST']['learning_rates']
        depths = [None] if 'default' in settings['CATBOOST']['depths'] else settings['CATBOOST']['depths']
        diffs = [define_diff(series)] if 'default' in settings['XGBOOST']['diff'] else settings['XGBOOST']['diff']
    
    for iteration in iterations:
        for learning_rate in learning_rates:
            for depth in depths:
                for diff in diffs:
                    cfg = [iteration, learning_rate, depth, diff]
                    models.append(cfg)

    return models
