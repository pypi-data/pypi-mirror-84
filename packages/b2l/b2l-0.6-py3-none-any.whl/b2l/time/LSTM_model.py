import numpy as np
from pandas import DataFrame, to_datetime, concat, DateOffset
from joblib import dump, load
from sklearn.preprocessing import RobustScaler
from tensorflow import keras
from datetime import datetime
from stories.model_list.base import rmse

def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)

def prepare_forecast_LSTM(train, test, columns, folder=None, settings=None):
    train = train.copy()
    test = test.copy()
    time_steps = {'M': 12, 'W': 12, 'D': 365}[columns['date_type']]

    rmse_test = test[columns['forecast']].values.flatten()
    test = concat([train[-time_steps:], test])

    train['month'] = train.index.month
    train['year'] = train.index.year

    if columns['date_type'] in ['D', 'W']:
        train['week'] = train.index.week

    f_transformer = RobustScaler()
    f_transformer = f_transformer.fit(train.loc[:, train.columns != columns['forecast']].to_numpy())
    train.loc[:, train.columns != columns['forecast']] = f_transformer.transform(train.loc[:, train.columns != columns['forecast']].to_numpy())
    cnt_transformer = RobustScaler()
    cnt_transformer = cnt_transformer.fit(train[[columns['forecast']]])
    train[columns['forecast']] = cnt_transformer.transform(train[[columns['forecast']]])

    X_df, y_df = create_dataset(train.loc[:, train.columns != columns['forecast']], train[columns['forecast']], time_steps)

    cfg_list = configs(settings)
    scores = []

    for cfg in cfg_list:
        prediction, model = train_LSTM(X_df, y_df, test, f_transformer, cnt_transformer, columns, time_steps, cfg)
        error = rmse(rmse_test, prediction)
        scores.append((cfg, error))
        best_score = cfg

    if len(scores) > 1:
        scores = [r for r in scores if r[1] != None]
        scores.sort(key=lambda tup: tup[1])
        best_score = scores[0][0]
        prediction, model = train_LSTM(X_df, y_df, test, f_transformer, cnt_transformer, columns, time_steps, best_score)


    epochs, batch_size = best_score
    model.reset_metrics()
    if folder is not None:
        model.save(folder + 'LSTM.h5')
        dump(f_transformer, folder + 'f_transformer.save')
        dump(cnt_transformer, folder + 'cnt_transformer.save')

    return (prediction, { 'model': model, 'f_transformer': f_transformer, 'cnt_transformer': cnt_transformer}, {'epochs': epochs, 'batch_size': batch_size}, [])

def future_forecast_LSTM(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
    time_steps = {'M': 12, 'W': 5, 'D': 365}[columns['date_type']]
    if df_forecast is None:
        if columns['date_type'] == 'D':
            old_dates = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(days=x-(time_steps-1)) for x in range(time_steps)]
            future_dates = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(days=x+1) for x in range(steps)]
        elif columns['date_type'] == 'W':
            old_dates = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(weeks=x-(time_steps-1)) for x in range(time_steps)]
            future_dates = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(weeks=x+1) for x in range(steps)]
        elif columns['date_type'] == 'M':
            old_dates = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(months=x-(time_steps-1)) for x in range(time_steps)]
            future_dates = [datetime.strptime(max_date, '%Y-%m-%d') + DateOffset(months=x+1) for x in range(steps)]
        future_dates = old_dates + future_dates
        df = DataFrame(data=future_dates, columns=['dates'])
        df.index = df['dates']
    else:
        df = df.loc[:, df.columns != columns['forecast']]
        df = concat([df.iloc[-time_steps:], df_forecast])

    df['month'] = df.index.month
    df['year'] = df.index.year

    if columns['date_type'] in ['D', 'W']:
        df['week'] = df.index.week

    if df_forecast is None:
        del df['dates']
        # df.index = to_datetime(df.index)
    else:
        df = df.reset_index()
        del df[columns['date']]

    if folder is not None:
        model_fit = keras.models.load_model(folder + 'LSTM.h5')
        f_transformer = load(folder + 'f_transformer.save')
        cnt_transformer = load(folder + 'cnt_transformer.save')
    else:
        model_fit = model['model']
        f_transformer = model['f_transformer']
        cnt_transformer = model['cnt_transformer']

    df.loc[:, :] = f_transformer.transform(df.loc[:, :].to_numpy())
    X_df, _ = create_dataset(df, df['year'], time_steps)

    predictions = model_fit.predict(X_df)
    predictions = cnt_transformer.inverse_transform(predictions)
    predictions = predictions.flatten()
    return predictions, []

def train_LSTM(X_df, y_df, test, f_transformer, cnt_transformer, columns, time_steps, config):
    epochs, batch_size = config
    
    model = keras.Sequential()
    model.add(keras.layers.Bidirectional(keras.layers.LSTM(units=128, input_shape=(X_df.shape[1], X_df.shape[2]))))
    model.add(keras.layers.Dropout(rate=0.2))
    model.add(keras.layers.Dense(units=1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_df, y_df, epochs=epochs, batch_size=batch_size, validation_split=0.1, shuffle=False,)
    
    test['month'] = test.index.month
    test['year'] = test.index.year

    if columns['date_type'] == 'D' or columns['date_type'] == 'W':
        test['week'] = test.index.week

    test.loc[:, test.columns != columns['forecast']] = f_transformer.transform(test.loc[:, test.columns != columns['forecast']].to_numpy())
    test[columns['forecast']] = cnt_transformer.transform(test[[columns['forecast']]])

    X_df, _ = create_dataset(test.loc[:, test.columns != columns['forecast']], test[columns['forecast']], time_steps)

    predictions = model.predict(X_df)
    predictions = cnt_transformer.inverse_transform(predictions)
    predictions = predictions.flatten()

    return (predictions, model)

def configs(settings):
    models = []
    if settings is None:
        epochs = [30]
        batch_size = [32]
    else:
        epochs = [30] if 'default' in settings['LSTM']['epochs'] else settings['LSTM']['epochs']
        batch_size = [32] if 'default' in settings['LSTM']['batch_size'] else settings['LSTM']['batch_size']
    
    for epoch in epochs:
        for batch in batch_size:
            cfg = [epoch, batch]
            models.append(cfg)
	
    return models