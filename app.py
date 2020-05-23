#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#plotly
import plotly.graph_objects as go
#data
import pandas as pd
import numpy as np
#api
import requests

# get the data
api = 'https://api.covid19india.org/data.json'
resp = requests.get(api)

caseTimeSeries = pd.DataFrame(resp.json()['cases_time_series'])  # timeseries data
stateWise = pd.DataFrame(resp.json()['statewise']) # statewise
tested = pd.DataFrame(resp.json()['tested']) # test statistics

#total statistics, Daily Cases trends 
fig = go.Figure()

fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totalconfirmed'], name='Total Confirmed'))
fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totalrecovered'], name='Total Recovered'))
fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totalconfirmed'].map(int)-caseTimeSeries['totalrecovered'].map(int), name='Total Active'))
fig.add_trace(go.Scatter(x=caseTimeSeries['date'], y=caseTimeSeries['totaldeceased'], name='Total Deceased'))
fig.add_trace(go.Bar(x=caseTimeSeries['date'], y=caseTimeSeries['dailyconfirmed'], name='Daily Confirmed'))
fig.add_trace(go.Bar(x=caseTimeSeries['date'], y=caseTimeSeries['dailydeceased'], name='Daily Deceased'))
fig.add_trace(go.Bar(x=caseTimeSeries['date'], y=caseTimeSeries['dailyrecovered'], name='Daily Recovered'))

fig.update_layout(barmode='stack')

#Doubling Rate
pctChange = pd.DataFrame({'date':caseTimeSeries['date'],'totalconfirmed':caseTimeSeries['totalconfirmed'],'pct_change':caseTimeSeries['totalconfirmed'].map(int).pct_change().mul(100).round(2)})
pctChange['cumul_pct'] = pctChange['pct_change'].cumsum()
p=1
rates = []
for i in range(100):
  if p > caseTimeSeries['totalconfirmed'].map(int).max():
    break
  else:
    rates.append(p)
    p = p *2

def doubling_rate(lst):
  # rates = rates
  tf = []
  for val in lst:
    try:
      if val >= rates[0]:
        # print (val, rates[0])
        rates.pop(0)
        
        tf.append(True)
      else:
        tf.append(False)
    except IndexError:
      # print (rates,len(rates))
      # print ('exception')
      tf.append(False)
  return tf

pctChange['double'] = doubling_rate(pctChange['totalconfirmed'].map(int))
pctChangenoDup = pctChange.drop_duplicates('cumul_pct',keep='last')
pctChangenoDup['double'] = doubling_rate(pctChange.drop_duplicates('cumul_pct',keep='last')['cumul_pct'])
doublingData = pctChange[pctChange['double']]
doublingData['doubleRate'] = doublingData.reset_index()['index'].diff().fillna(0).to_list()

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=doublingData['date'],y=doublingData['doubleRate'], name='DoublingRate of Cases'))
fig2.add_trace(go.Scatter(x=doublingData['date'],y=doublingData['doubleRate'], name='DoublingRate of Cases'))
fig2.add_trace(go.Scatter(x=doublingData['date'],y=doublingData['totalconfirmed'].map(int).map(np.log), name='Total Cases LogScale'))
fig2.update_layout(title='Doubling Rate of Cases in India ' + str(doublingData['doubleRate'].iloc[-1]))


url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
    
    
########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title="Cov19India"

layout_index = html.Div([
    dcc.Link('Navigate to "covid19India"', href='/covid19'),
    html.Br(),
    dcc.Link('Navigate to "/blog"', href='/blog'),
])

    
covid_layout= html.Div(children=[
    html.H2("Total Cases TrendLine - India"),
    dcc.Graph(
        id='Cov1',
        figure=fig
    ),
    html.H2("Doubling Rate of Cases"),
    dcc.Graph(
        id='Cov2',
        figure=fig2
    ),
    html.A('Code on Github', href='https://github.com/phanikiran99/cov19India'),
    html.Br(),
    html.A('Data Source', href='covid19india.org'),
    ]
)


    
blog_layout = html.Div([
    html.H2('Blog'),
    #dcc.Dropdown(
    #    id='page-2-dropdown',
    #    options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
    #    value='LA'
    #),
    #html.Div(id='page-2-display-value'),
    #html.Br(),
    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    dcc.Link('Navigate to "/covid19india"', href='/covid19'),
])    
# index layout
app.layout = url_bar_and_content_div

# "complete" layout
app.validation_layout = html.Div([
    url_bar_and_content_div,
    layout_index,
    covid_layout,
    blog_layout,
])    

# Index callbacks
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/covid19":
        return covid_layout
    elif pathname == "/blog":
        return blog_layout
    else:
        return layout_index


    
if __name__ == '__main__':
    app.run_server()
