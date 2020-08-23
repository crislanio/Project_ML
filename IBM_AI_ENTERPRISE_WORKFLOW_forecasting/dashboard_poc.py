#!/usr/bin/env python

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import plotly.graph_objs as go

import pandas as pd
import numpy as np
import requests
from dateutil.relativedelta import relativedelta
from ast import literal_eval
import datetime
import time


# r = requests.post("http://localhost:8080/predict_all_datetime", json={"begin" : 1558915200000, "end": 1590447600000 },  verify=False)          # timestamp test
r = requests.post("http://localhost:8080/predict_all_datetime", json={"begin" : "1990-01", "end": "2100-01" },  verify=False)
# print(r.json())
# print('dash here ', r.json())

df = pd.DataFrame.from_dict(r.json(), orient="columns") 
min_range = df.ds.min()
max_range = df.ds.max()
print(min_range, max_range)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

# df = pd.DataFrame(eval(r.json()))
df = pd.DataFrame.from_dict(r.json(), orient="columns") 
print('df dash', df.head(1))
df['average_line'] =  np.mean( df['yhat'] )


    # Updating the plot
    # Create a plotly figure
trace = go.Scatter(
            name = 'Runtime Value',
        # mode = 'markers',
        mode = 'lines',
        x = list( df['ds'] ),
        y = list( df['yhat']),
        marker=dict(
                color='#007DB8',
                line=dict(width=1)
        )
    )

trace1 = go.Scatter(
        name = 'Trend line',
        mode = 'lines',
        x = list(df['ds']),
        y = list(df['trend']),
        marker=dict(
                color='purple',
                line=dict(width=1)
        )
    )
trace1_avg = go.Scatter(
        name = 'Average line',
        mode = 'lines',
        x = list(df['ds']),
        y = list(df['average_line']),
        marker=dict(
                color='red',
                line=dict(width=1)
        )
    )


layout = dict(title='Aavail Demand Revenue Forecast',
                xaxis=dict(title = 'Date Time', ticklen=2, zeroline=False))
fig= dict(data= [trace, trace1, trace1_avg] ,layout=layout)    
 
# fig = px.scatter(df, x="ds", y="yhat")
# fig.update_layout(transition_duration=500)

app.layout = html.Div(children=[
    html.H1(children='Aavail dashboard POC'),

    html.Div(children='''
        Demand Revenue Forecast
    '''),

    dcc.Graph(id='poc_dash',figure=fig)
])


# app.layout = html.Div([

#             # a header and a paragraph
#                 html.Div([
#                         html.Label(['Aavail dashboard POC'],
#                                     style={'padding' : '30px' ,'backgroundColor' : '#007DB8','font-weight': 'bold','fontSize' : '25px'}),
#                 html.P(),

#                                 # adding a plot
#                 html.Div([
#                     dcc.Graph(id='graph-with-slider')
#                 ])                
                
#     ])
# ])    


if __name__ == '__main__':
    app.run_server(debug=True)