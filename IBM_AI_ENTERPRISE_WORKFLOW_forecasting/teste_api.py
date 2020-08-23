#!/usr/bin/python           
import argparse
import requests
from flask import Flask, jsonify, request
from flask import render_template, send_from_directory
# import os
# import re
import joblib
# import socket
import json
import numpy as np
import pandas as pd
from ast import literal_eval
# from prophet_model import model_train, model_predict, model_predict_country


def test_API_running():
    ## ping the API
    port = 8080    
    r = requests.post('http://localhost:{}/running'.format(port))
    response = r.text
    # response = literal_eval(r.text)
    return response

def predict_all_datetime(request_json):
    ## ping the API
    port = 8080    
    r = requests.post('http://localhost:{}/predict_all_datetime'.format(port),json=request_json)
    response = r.text
    return response


def test_API_predict(request_json):
    ## ping the API
    port = 8080    
    # request_json = {'country':'netherlands','year':'2019','month':'01','day':'05'}
    # print('teste ', request_json[0])
    r = requests.post('http://localhost:{}/predict'.format(port),json=request_json)
    response = r.text
    # response = literal_eval(r.text)
    return response

def test_API_predict_all(request_json_all):
    ## ping the API
    port = 8080    
    r = requests.post('http://localhost:{}/predict_all'.format(port),json=request_json_all)
    # response = r.text
    response = literal_eval(r.text)
    # df = pd.DataFrame(eval(r.json()))
    # print(df.info())
    # print(df.head())
    # print(response)
    # print('type ',type(response))
    return response #"test forecast country"



if __name__ == "__main__":
    request_json = {'country':'netherlands','year':'2019','month':'01','day':'05'}

    # request_json_datetime = {"begin" : 1558915200000, "end": 1590447600000 }
    request_json_datetime = {"begin" : "1990-01", "end": "2100-01" }
    request_json_all = {'country':'spain'}

    # ### endpoint running
    # print("test API - endpoint running")
    # res_running = test_API_running()
    # print(res_running)

    ### endpoint predict_all_datetime
    # print("test API - endpoint predict_all_datetime")
    # predict_datetime = predict_all_datetime(request_json_datetime)
    # print(predict_datetime)


    # ### endpoint predict
    # print("test API - endpoint predict")
    # res_predict = test_API_predict(request_json)
    # print(res_predict)

    ### endpoint predict_all
    # print("test API - endpoint predict_all")
    # predict_all = test_API_predict_all(request_json_all)
    # print(predict_all)

    # result = model_predict("netherlands","2018","12","10") 
    # print('teste2 ',result.yhat.values[0])
    
