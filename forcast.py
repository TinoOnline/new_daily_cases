import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import json



def forecast(dates, cases):
    df = preprocessing(dates, cases)    
    model_forcast = ARIMA(df['cases'], order=(10, 0, 1))
    model_forcast_fit = model_forcast.fit()
    test_forecast_new = model_forcast_fit.forecast(steps=7)
    plt.figure(figsize=(14,7))
    plt.plot(df['cases'], label='Historical Data')
    plt.plot(test_forecast_new, label='Forecasted 7 Days', color='green')
    plt.title('ARIMA Model Forecast 7 Days')
    plt.xlabel('Date')
    plt.ylabel('Reported Cases')
    plt.legend()
    plt.savefig('forecast.png')
    plt.close()
    df = pd.DataFrame({'date': test_forecast_new.index.strftime('%Y-%m-%d'), 'new_cases': test_forecast_new.values})
    df['new_cases'] = df['new_cases'].astype(int)
    df.to_csv("new_cases", sep=',',index=False)
    return json.dumps(df.to_json(orient="records"))

# This function deterimines the index where there are still values in the dataset, beyond this point it's zeroes.
# We do not want to simply remove the zeroes in the core of the data
def end_index(cases):
    i = 0
    for elem in reversed(cases):
        if elem > 0:
            break
        i += 1
    return len(cases)-i


def preprocessing(dates, cases):
    limit_index = end_index(cases)
    covid_cases = { "dates":dates[:limit_index], "cases":cases[:limit_index]}
    df = pd.DataFrame(data=covid_cases)
    df['dates'] = pd.to_datetime(df['dates'])
    df = df[df.cases.notnull()]
    # use capital letters, name it to cases
    # check what parameters you can load on data importing, without explicitly defining the steps

     #This function is used to smooth out the data and remove any internal zeros in the function, this is important in order to carry out the adffuller test
    series = df['cases']
    filled_series = series.copy()
    rolling_mean = series.rolling(window=7, min_periods=1, center=True).mean()
    mask = df["cases"] == 0
    filled_series[mask] = rolling_mean[mask]
    df["cases"] = filled_series

    mask = (df['dates'] > '2022-06-17')
    df = df.loc[mask]
    df.set_index('dates', inplace=True)
    #Towards the end of the pandemic the tred was stable and had less pronounced seasonal variation. This would skew the short term prediciton that needs to be made hence this data needed to be excluded in using this methematical model
    # 2022-06-21 Cut off is a resut of the end of the previous sparodic behaviour, looking at the gentle forecast going forward

    return df