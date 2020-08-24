# !/usr/bin/env python

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

# req = {"country":"netherlands" ,"begin" : "2019-01", "end": "2019-02" }  # test interval date

# req = {"country":"netherlands" ,"begin" : "2000-01", "end": "2100-01" }
# req_ = {"country":"netherlands"}

country_param = "spain" 
begin_param = "2000-01"
end_param = "2100-01"
req = {"country": country_param,"begin" : begin_param, "end": end_param }
req_ = {"country":country_param}


r = requests.post("http://localhost:8080/predict_all_datetime", json=req,  verify=False)

r_ = requests.post("http://localhost:8080/countrylist", json=req_,  verify=False)

# r = requests.post("http://localhost:8080/predict_all_datetime", json={"country":"spain" ,"begin" : "2000-01", "end": "2100-01" },  verify=False)

df_ = pd.DataFrame.from_dict(r_.json(), orient="columns") 
# print('countries df ',df_.head())
# print('teste :', df_.loc[df_['countries']=='netherlands'].values[0][0] )

df = pd.DataFrame.from_dict(r.json(), orient="columns") 
min_range = df.ds.min()
max_range = df.ds.max()
print(min_range, max_range)
# print("r json ", r.json())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

colors = {
    'background': '#purple',
    'text': '#7FDBFF'
}

# df = pd.DataFrame(eval(r.json()))
df = pd.DataFrame.from_dict(r.json(), orient="columns") 
# print('df dash', df.head(1))
df['average_line'] =  np.mean( df['yhat'] )


def generate_table(dataframe, max_rows=10):  # poc test, max 10 lines
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])



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


layout = dict(title='Aavail Demand Revenue Forecast for {} '.format( df_.loc[df_['countries']==req_['country']].values[0][0] ),
                xaxis=dict(title = 'Date Time', ticklen=2, zeroline=False))
fig= dict(data= [trace, trace1, trace1_avg] ,layout=layout)    
 
 
app.layout = html.Div(style={'backgroundColor': colors['background']},   children=[
    html.H1(children='Aavail dashboard POC'),

    html.Div(children='''
        Demand Revenue Forecast
    '''),

    dcc.Graph(id='poc_dash',figure=fig),

    html.H4(children='Table Stats'),
    generate_table(df[['ds','trend','yhat','yhat_lower','yhat_upper']])
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