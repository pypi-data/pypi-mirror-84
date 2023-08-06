from warnings import filterwarnings, catch_warnings
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from b2l.base import rmse
from joblib import dump, load
from datetime import datetime
from pandas import DateOffset, Series

def prepare_forecast_HWES(train, test, columns, folder=None, settings=None):
	train, test = train[columns['forecast']].values.flatten(), test[columns['forecast']].values.flatten()
	cfg_list = configs(columns['date_type'], settings)
	scores = []

	for cfg in cfg_list:
		error = None
		try:
			with catch_warnings():
				filterwarnings("ignore")
				predictions, model = train_HWES(train, cfg, len(test))
				error = rmse(test, predictions)
		except:
			error = None
		# predictions, model = train_HWES(train, cfg, len(test))
		# error = rmse(test, predictions)

		if error is not None:
			print(' > Model[%s] %.3f' % (str(cfg), error))
		
		scores.append((cfg, error))
		best_score = cfg

	if len(scores) > 1:
		scores = [r for r in scores if r[1] != None]
		scores.sort(key=lambda tup: tup[1])
		best_score = scores[0][0]
		print('best_score is ' + str(best_score))
		prediction, model = train_HWES(train, best_score, len(test))
	
	trend, damped, seasonal, seasonal_periods, boxcox, bias = best_score
	if folder is not None:
		dump(model, folder + 'HWES.save')
	return (prediction, model, {'trend': trend, 'damped': damped, 'seasonal': seasonal, 'seasonal_periods': seasonal_periods, 'boxcox': boxcox, 'bias': bias}, [])

# def future_forecast_HWES(steps, max_date, folder, date_type, df, forecast_column):
def future_forecast_HWES(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):
	if folder is not None:
		model = load(folder + 'HWES.save')
	max_date = datetime.strptime(max_date, '%Y-%m-%d')

	if df_forecast is not None:
		steps = len(df_forecast)

	if columns['date_type'] == 'H':
		test_period = Series([max_date - DateOffset(hours=x+1) for x in range(365*24)])
	elif columns['date_type'] == 'D':
		test_period = Series([max_date - DateOffset(days=x+1) for x in range(365)])
	elif columns['date_type'] == 'W':
		test_period = Series([max_date - DateOffset(weeks=x+1) for x in range(52)])
	elif columns['date_type'] == 'M':
		test_period = Series([max_date - DateOffset(months=x+1) for x in range(12)])
	elif columns['date_type'] == 'Q':
		test_period = Series([max_date - DateOffset(quarters=x+1) for x in range(4)])
	elif columns['date_type'] == 'Y':
		test_period = Series([max_date - DateOffset(years=x+1) for x in range(1)])

	test_period = test_period[test_period.dt.year == max_date.year]
	test_period = len(test_period) + 1
	if (columns['date_type'] == 'D' and test_period < 365) or (columns['date_type'] == 'W' and test_period < 52) or (columns['date_type'] == 'M' and test_period < 12):
		period = test_period
	else:
		period = 0

	prediction = model.forecast(steps=period+steps)
	prediction = prediction[-steps:]
	return prediction, []

def train_HWES(train, config, step):
	t, d, s, p, b, r = config
	model = ExponentialSmoothing(endog=train, trend=t, damped=d, seasonal=s, seasonal_periods=p)
	model_fit = model.fit(optimized=True, use_boxcox=b, remove_bias=r)
	prediction = model_fit.forecast(steps=step)
	return (prediction, model_fit)

def configs(date_type, settings):
	models = []
	p_params = {'M': [12], 'D': [365], 'W': [52], 'Y': [1], 'Q': [4]}[date_type]

	if settings is None:
		t_params = ['add', 'mul', None]
		d_params = [True, False]
		s_params = ['add', 'mul', None]
		b_params = [True, False]
		r_params = [True, False]
	else:
		t_params = ['add', 'mul', None] if 'default' in settings['HWES']['trend'] else settings['HWES']['trend']
		d_params = [True, False] if 'default' in settings['HWES']['damped'] else settings['HWES']['damped']
		s_params = ['add', 'mul', None] if 'default' in settings['HWES']['seasonal'] else settings['HWES']['seasonal']
		b_params = [True, False] if 'default' in settings['HWES']['boxcox'] else settings['HWES']['boxcox']
		r_params = [True, False] if 'default' in settings['HWES']['bias'] else settings['HWES']['bias']
	
	for t in t_params:
		for d in d_params:
			for s in s_params:
				for p in p_params:
					for b in b_params:
						for r in r_params:
							cfg = [t, d, s, p, b, r]
							models.append(cfg)
	return models
