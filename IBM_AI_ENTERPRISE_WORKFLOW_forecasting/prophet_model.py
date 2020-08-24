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
import numpy as np
import random
from sklearn.metrics import mean_squared_error, mean_absolute_error

MODEL_VERSION = 0.1
MODEL_VERSION_NOTE = "Prophet"


def prophet_model_tuning(country):  
    #### see this : https://www.kaggle.com/manovirat/timeseries-using-prophet-hyperparameter-tuning    
    from sklearn.model_selection import ParameterGrid
    params_grid = {'seasonality_mode':('multiplicative','additive')
    #                ,'changepoint_prior_scale':[0.1,0.3,0.5]
    #           'n_changepoints' : [100,200]
                }
    grid = ParameterGrid(params_grid)


    data_dir = os.path.join("data","cs_train","data")
    ts_data = fetch_ts(data_dir)
    countries=[]
    for c,df in ts_data.items():
        countries.append(c)

    if(country not in countries):
        text="Could not find country called "+ country+".csv"
        return(text)
    else:
        filename="./data/cs_train/data/ts-"+country+".csv"
        df = pd.read_csv(filename)
    # # test import data
    # country = "spain"
    # filename="./data/cs_train/data/ts-"+country+".csv"
    # df = pd.read_csv(filename)
    # print( df.date.min(),df.date.max())    

        df.rename( columns={'date':'ds', 'revenue':'y'}, inplace=True)
        X = df[['ds','y']].copy()
        size = int(len(X) * 0.70)
        train, test = X[0:size], X[size:]

        # strt =   df.ds.min()
        # end  =   df.iloc[size]['ds']
        end_  =   df.iloc[train.shape[0]+60]['ds']   # test cv data

        model_parameters = pd.DataFrame(columns = ['MSE','Parameters'])
        for p in grid:
            test_ = pd.DataFrame()
            # print(p)
            random.seed(0)
            train_model =Prophet(
        #         changepoint_prior_scale = p['changepoint_prior_scale'],
        #                          n_changepoints = p['n_changepoints'],
                                seasonality_mode = p['seasonality_mode'],
                                weekly_seasonality=True,
                                daily_seasonality = True,
                                yearly_seasonality = True,
                                interval_width=0.95)
            train_model.fit(train)
            train_forecast = train_model.make_future_dataframe(periods=60, freq='D',include_history = False)
            train_forecast = train_model.predict(train_forecast)
            
            test_=train_forecast[['ds','yhat']]
            Actual = df[(df['ds']> train.ds.max()) & (df['ds']< end_)]
            
            
            MSE = mean_squared_error(Actual['y'],abs(test_['yhat']))
            print('      Start: Tuning model                                 ')
            print('Mean Square Error(MSE)------------------------------------',MSE)
            model_parameters = model_parameters.append({'MSE':MSE,'Parameters':p},ignore_index=True)  
            print('      Finished: Tuning model                                 ')
            
            return model_parameters.to_dict()


def model_train_cv(country_):
    ## start timer for runtime
    time_start = time.time()
    data_dir = os.path.join("data","cs_train","data")
    ts_data = fetch_ts(data_dir)
    
    parameters = prophet_model_tuning(country_)
    for country,df in ts_data.items():
        m =Prophet(
#                changepoint_prior_scale = parameters['Parameters'][0]['changepoint_prior_scale'],
#                n_changepoints = parameters['Parameters'][0]['n_changepoints'],
                 seasonality_mode = parameters['Parameters'][0]['seasonality_mode'],
                 weekly_seasonality=True, daily_seasonality = True, yearly_seasonality = True,interval_width=0.95)
            
        df2=df[["date","revenue"]]
        df2.columns = ['ds', 'y']
        m.fit(df2)
        future = m.make_future_dataframe(periods=120) # predict future, 120 days
        forecast = m.predict(future)
        forecast['country'] = country
        
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        filename="data/forecasts/forecast_" + country+".csv"
        forecast.to_csv(filename)
    
    ## update the log file
    m, s = divmod(time.time()-time_start, 60)
    h, m = divmod(m, 60)
    runtime = "%03d:%02d:%02d"%(h, m, s)
    test=False
    update_train_log(forecast.shape, runtime, MODEL_VERSION, MODEL_VERSION_NOTE, test)

    return parameters 

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
        forecast['country'] = country
        
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

def _country_list(country):
    data_dir = os.path.join("data","cs_train","data")
    ts_data = fetch_ts(data_dir)
    countries=[]
    for c,df in ts_data.items():
        countries.append(c)

    if(country not in countries):
        text="Could not find country called in the list of countries"
        return(text)

    else:
        countries_df = pd.DataFrame()        
        countries_df['countries'] = countries
        filename="./data/forecasts/countries.csv"
        countries_df.to_csv(filename, index=False)
        countries_df = pd.read_csv(filename)
        return countries_df

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

def predict_all_datetime_model(country):
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
        return forecasts[['ds','trend','yhat','yhat_lower','yhat_upper']] #.to_json(orient="columns")

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

    # print(model_predict("netherlands","2020","12","10"))
    # print(model_predict("spain","2018","10","01"))   
    # print(model_predict("spain","2019","06","23"))   
    # print(model_predict("spain","2019","06","24"))   
    
    # print(model_predict("all","2018","01","01"))          # show forecast row for a country and date


    model_train_cv("spain")   # test tuning fb propeth

    # print(_country_list("spain"))   # list coutries
    # print(_country_list("peru"))   # list coutries
