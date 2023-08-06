from .time.SARIMAX_model import prepare_forecast_SARIMAX, future_forecast_SARIMAX
from .time.AUTO_SARIMAX_model import prepare_forecast_AUTO_SARIMAX, future_forecast_AUTO_SARIMAX
from .time.PROPHET_model import prepare_forecast_PROPHET, future_forecast_PROPHET
from .time.HWES_model import prepare_forecast_HWES, future_forecast_HWES
from .time.XGBOOST_model import prepare_forecast_XGBOOST, future_forecast_XGBOOST
from .time.CATBOOST_model import prepare_forecast_CATBOOST, future_forecast_CATBOOST
from .time.LIGHTGBM_model import prepare_forecast_LIGHTGBM, future_forecast_LIGHTGBM
from .time.LSTM_model import prepare_forecast_LSTM, future_forecast_LSTM
from b2l.time.YTY_model import prepare_forecast_YTY, future_forecast_YTY
from .time.AR_model import prepare_forecast_AR, future_forecast_AR

class Models:
    def __init__(self, model, forecast_type='time'):
        self.model = model
        self.forecast_type = forecast_type
        self.model_fit = None
        self.best_config = None
        self.columns = None

    def train(self, train, test, columns):
        model_forecast, model, best_config, baseline = globals()['prepare_forecast_' + self.model](train=train, test=test, columns=columns)
        self.model_fit = model
        self.best_config = best_config
        self.columns = columns
        return model_forecast, baseline

    def forecast(self, steps, max_date, df, df_forecast=None):
        prediction, baseline = globals()['future_forecast_' + self.model](steps=steps, max_date=max_date, columns=self.columns, best_config=self.best_config, model=self.model_fit, df=df, df_forecast=df_forecast)
        return prediction, baseline