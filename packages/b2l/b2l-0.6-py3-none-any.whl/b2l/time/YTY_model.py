from numpy import append
from joblib import dump, load

def prepare_forecast_YTY(train, test, columns, folder=None, settings=None):

    if columns['date_type'] == 'M':
        test_months = test.index.max().month
        if test_months == 12:
            year_growth = test.values.sum()/train[-12:].values.sum()
            prediction = train[-12:].values * year_growth
        else:
            year_growth = test.values.sum()/train[-12:-(12-test_months)].values.sum()
            prediction = train[-12:-(12-test_months)].values * year_growth

    if columns['date_type'] == 'W':
        test_weeks = test.index.max().week
        if test_weeks == 52:
            year_growth = test.values.sum()/train[-52:].values.sum()
            prediction = train[-52:].values * year_growth
        else:
            year_growth = test.values.sum()/train[-52:-(52-test_weeks)].values.sum()
            prediction = train[-52:-(52-test_weeks)].values * year_growth

    if columns['date_type'] == 'D':
        test_days = test.index.max().dayofyear
        if test_days == 365:
            year_growth = test.values.sum()/train[-365:].values.sum()
            prediction = train[-365:].values * year_growth
        else:
            year_growth = test.values.sum()/train[-365:-(365-test_days)].values.sum()
            prediction = train[-365:-(365-test_days)].values * year_growth

    if folder is not None:
        dump({'year_growth': year_growth}, folder + 'YTY.save')
    return (prediction, {'year_growth': year_growth}, {}, [])

def future_forecast_YTY(steps, max_date, columns, best_config, model, df=None, df_forecast=None, folder=None):

    if folder is not None:
        config = load(folder + 'YTY.save')
        year_growth = config['year_growth']
    else:
        year_growth = model['year_growth']
        
    prediction = []

    if columns['date_type'] == 'M':
        max_month = df[columns['date']].max().month
        if max_month < 12:
            if steps <= 12 - max_month:
                prediction = df[columns['forecast']][-12:-(12-steps)].values * year_growth
            else:
                prediction = df[columns['forecast']][-12:-max_month].values * year_growth
                steps = steps - (12 - max_month)
                years = steps // 12
                semi_year = steps % 12
                first_year = append(df[columns['forecast']][-max_month:].values, prediction)
                if years == 0:
                    prediction = append(prediction, first_year[:semi_year] * year_growth)
                else:
                    for year in range(years):
                        if year + 1 == 1:
                            prediction = first_year * year_growth
                        else:
                            prediction = append(prediction, prediction[-12:] * year_growth)
                    if semi_year != 0:
                        prediction = append(prediction, prediction[-12:(semi_year - 12)] * year_growth)

        else:
            years = steps // 12
            semi_year = steps % 12
            if years == 0:
                prediction = df[columns['forecast']][-12:(steps - 12)].values * year_growth
            else:
                for year in range(years):
                    if year + 1 == 1:
                        prediction = df[columns['forecast']][-12:].values * year_growth
                    else:
                        prediction = append(prediction, prediction[-12:] * year_growth)
                if semi_year != 0:
                    prediction = append(prediction, prediction[-12:(semi_year - 12)] * year_growth)

    if columns['date_type'] == 'W':
        max_week = df[columns['date']].max().week
        if max_week < 52:
            if steps <= 52 - max_week:
                prediction = df[columns['forecast']][-52:-(52-steps)].values * year_growth
            else:
                prediction = df[columns['forecast']][-52:-max_week].values * year_growth
                steps = steps - (52 - max_week)
                years = steps // 52
                semi_year = steps % 52
                first_year = append(df[columns['forecast']][-max_week:].values, prediction)
                if years == 0:
                    prediction = append(prediction, first_year[:semi_year] * year_growth)
                else:
                    for year in range(years):
                        if year + 1 == 1:
                            prediction = first_year * year_growth
                        else:
                            prediction = append(prediction, prediction[-52:] * year_growth)
                    if semi_year != 0:
                        prediction = append(prediction, prediction[-52:(semi_year - 52)] * year_growth)

        else:
            years = steps // 52
            semi_year = steps % 52
            if years == 0:
                prediction = df[columns['forecast']][-52:(steps - 52)].values * year_growth
            else:
                for year in range(years):
                    if year + 1 == 1:
                        prediction = df[columns['forecast']][-52:].values * year_growth
                    else:
                        prediction = append(prediction, prediction[-52:] * year_growth)
                if semi_year != 0:
                    prediction = append(prediction, prediction[-52:(semi_year - 52)] * year_growth)

    if columns['date_type'] == 'D':
        max_day = df[columns['date']].max().dayofyear
        if max_day < 365:
            if steps <= 365 - max_day:
                prediction = df[columns['forecast']][-365:-(365-steps)].values * year_growth
            else:
                prediction = df[columns['forecast']][-365:-max_day].values * year_growth
                steps = steps - (365 - max_day)
                years = steps // 365
                semi_year = steps % 365
                first_year = append(df[columns['forecast']][-max_day:].values, prediction)
                if years == 0:
                    prediction = append(prediction, first_year[:semi_year] * year_growth)
                else:
                    for year in range(years):
                        if year + 1 == 1:
                            prediction = first_year * year_growth
                        else:
                            prediction = append(prediction, prediction[-365:] * year_growth)
                    if semi_year != 0:
                        prediction = append(prediction, prediction[-365:(semi_year - 365)] * year_growth)

        else:
            years = steps // 365
            semi_year = steps % 365
            if years == 0:
                prediction = df[columns['forecast']][-365:(steps - 365)].values * year_growth
            else:
                for year in range(years):
                    if year + 1 == 1:
                        prediction = df[columns['forecast']][-365:].values * year_growth
                    else:
                        prediction = append(prediction, prediction[-365:] * year_growth)
                if semi_year != 0:
                    prediction = append(prediction, prediction[-365:(semi_year - 365)] * year_growth)

    return prediction, []
