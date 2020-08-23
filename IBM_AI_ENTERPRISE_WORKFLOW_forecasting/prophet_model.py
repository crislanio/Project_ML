#!/usr/bin/python           
""" 
In this file, the functions for training and predicting with Prophet are defined.
"""

import os
import pandas as pd
from fbprophet import Prophet
from cslib import fetch_ts
import re
from logger import update_predict_log, update_train_log
import time

MODEL_VERSION = 0.1
MODEL_VERSION_NOTE = "Prophet"

def model_train():
    ## start timer for runtime
    time_start = time.time()
    data_dir = os.path.join("data","cs_train","data")
    ts_data = fetch_ts(data_dir)

    for country,df in ts_data.items():
        m = Prophet()
        df2=df[["date","revenue"]]
        df2.columns = ['ds', 'y']
        m.fit(df2)
        future = m.make_future_dataframe(periods=120) # predict future, 120 days
        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        filename="data/forecasts/forecast_" + country+".csv"
        forecast.to_csv(filename)
    
    ## update the log file
    m, s = divmod(time.time()-time_start, 60)
    h, m = divmod(m, 60)
    runtime = "%03d:%02d:%02d"%(h, m, s)
    test=False
    update_train_log(forecast.shape, runtime, MODEL_VERSION, MODEL_VERSION_NOTE, test)

    return True

def model_predict_country(country):
    time_start = time.time()
    data_dir = os.path.join("data","cs_train","data")
    ts_data = fetch_ts(data_dir)
    countries=[]
    for c,df in ts_data.items():
        countries.append(c)

    if(country not in countries):
        text="Could not find country called "+ country+".csv"
        return(text)

    else:
        filename="./data/forecasts/forecast_"+country+".csv"
        forecasts = pd.read_csv(filename)
        # print('type df',type(forecasts))
        # return forecasts#.to_json() #file_fc
        return forecasts [['ds','trend','yhat','yhat_lower','yhat_upper']]

def model_predict(country, year, month, day):
    time_start = time.time()
    data_dir = os.path.join("data","cs_train","data")
    ts_data = fetch_ts(data_dir)
    countries=[]
    for c,df in ts_data.items():
        countries.append(c)

    if(country not in countries):
        text="Could not find country called "+ country+".csv"
        return(text)

    else:
        filename="./data/forecasts/forecast_"+country+".csv"
        forecasts = pd.read_csv(filename)
        date_str=year + "-" + month + "-" + day
        row=forecasts.loc[forecasts['ds'] == date_str]
    
    
    if(len(row)==0):
        return "Date not available"
    else:
        # update the log file
        m, s = divmod(time.time()-time_start, 60)
        h, m = divmod(m, 60)
        runtime = "%03d:%02d:%02d"%(h, m, s)
        test=False
        update_predict_log(row.yhat.values[0],runtime,MODEL_VERSION,MODEL_VERSION_NOTE, test)
        return row

if __name__ == "__main__":

    # model_train()

    print(model_predict("netherlands","2020","12","10"))
    print(model_predict("spain","2018","10","05"))    
    print(model_predict("all","2018","01","01"))          # show forecast row for a country and date

    # print(model_predict_country("spain"))  # show forecast data for a country
