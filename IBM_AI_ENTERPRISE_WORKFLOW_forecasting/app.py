#!/usr/bin/python    
       
import argparse
import requests
from flask import Flask, jsonify, request
from flask import render_template, send_from_directory
import os
import re
import joblib
import socket
import json
import numpy as np
import pandas as pd
from prophet_model import model_train, model_predict, model_predict_country, predict_all_datetime_model, _country_list, model_train_cv

app = Flask(__name__)

# filename="./data/forecasts/forecast_singapore.csv"
# filename="./data/forecasts/forecast_all.csv"
# filename="./data/forecasts/forecast_spain.csv"
# df = pd.read_csv(filename)
# test_poc = df [['ds','trend','yhat','yhat_lower','yhat_upper']].copy()


@app.route('/countrylist', methods=['GET','POST'])
def country_list():
    ## extract the query
    query = request.json
    c=query.get("country")
    country_list = _country_list(c)
    return country_list.to_json(orient="columns")

@app.route('/running', methods=['GET','POST'])
def running():
    return jsonify(True)


@app.route('/predict_all_datetime', methods=['GET','POST'])
def predict_all_datetime():
    if not request.json:
        print("ERROR: API (predict): did not receive request data")
        return jsonify([])
    
    else:
        ## extract the query
        query = request.json

        c=query.get("country")
        print(c)
        # print('query ',query)        
        print('query type ',type(query))

        test_poc = predict_all_datetime_model(c)
        # return (jsonify(result))
        # return result.to_json(orient="columns")

        return test_poc[(test_poc['ds'] > query['begin']) & \
                        (test_poc['ds'] <= query['end'])].to_json(orient="columns")


@app.route('/predict_all', methods=['GET','POST'])
def predict_all():
    """
    basic predict function for the API
    """
    ## input checking
    if not request.json:
        print("ERROR: API (predict): did not receive request data")
        return jsonify([])

    if 'country' not in request.json:
        print("ERROR API (predict): received request, but no country found within")
        return jsonify([])

    ## extract the query
    query=(request.json)
    c=query.get("country")
    print(c)
    print('query ',query)        
    print('query type ',type(query))

    result = model_predict_country(c)
    # return (jsonify(result))
    return result.to_json(orient="columns")



@app.route('/predict', methods=['GET','POST'])
def predict():
    """
    basic predict function for the API
    """
    
    ## input checking
    if not request.json:
        print("ERROR: API (predict): did not receive request data")
        return jsonify([])

    if 'country' not in request.json:
        print("ERROR API (predict): received request, but no country found within")
        return jsonify([])

    if 'year' not in request.json:
        print("ERROR API (predict): received request, but no year found within")
        return jsonify([])

    if 'month' not in request.json:
        print("ERROR API (predict): received request, but no month found within")
        return jsonify([])
        
    if 'day' not in request.json:
        print("ERROR API (predict): received request, but no day found within")
        return jsonify([])

    ## extract the query
    query=(request.json)
    c=query.get("country")
    y=query.get("year")
    m=query.get("month")
    d=query.get("day")
    print(c,y,m,d)

    print('query ',query)        
    print('query type ',type(query))

    result = model_predict(c,y,m,d)
    return(jsonify(result.yhat.values[0]))


@app.route('/tuningmodel', methods=['GET','POST'])
def tuningmodel():
    """
    basic tuningmodel function for the API
    """
    ## input checking
    if not request.json:
        print("ERROR: API (predict): did not receive request data")
        return jsonify([])

    if 'country' not in request.json:
        print("ERROR API (predict): received request, but no country found within")
        return jsonify([])

    print("... tuningmodel model")
    ## extract the query
    query=(request.json)
    c=query.get("country")
    result = model_train_cv(c)
    print("... tuning model complete")
    return(jsonify(result))

@app.route('/train', methods=['GET','POST'])
def train():
    """
    basic predict function for the API
    """

    print("... training model")
    model_train()
    print("... training complete")

    return(jsonify(True))
        
if __name__ == '__main__':

    ## parse arguments for debug mode
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="debug flask")
    args = vars(ap.parse_args())

    if args["debug"]:
        app.run(debug=True, port=8080)
    else:
        app.run(host='0.0.0.0', threaded=True ,port=8080)

