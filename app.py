#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import plots
import geo
#import base64
import os
import flask
import pathlib
import helper

#import sqlite3

cat = []  #categories
titles= [] #titles
for arti in helper.retriveArticlesList():
    print(arti[0],arti[3])
    cat.append({'label':arti[0],'value':arti[0]})
    titles.append({'label':arti[3],'value':arti[3]})
print(cat,titles)
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()



geo.saveImages();

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

    
########### Initiate the app
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
server = app.server
app.title="Phani-Writes"

layout_index = html.Div([
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("bitmap.png"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",
                                "margin-bottom": "0px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Phani - Works",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Some Naive Analytics", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="#",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
    
    html.Div(
            [
            html.Div([
                    html.Div([html.P("Category"),dcc.Dropdown(options=cat,multi=True),]),
                      html.Div([html.P("Title"),dcc.Dropdown(options=titles,multi=True),]),
                      ],className='pretty-container col-md-3'),
            html.Div(
                    [
                    html.H6("Covid19"),
                    html.P('Covid19 India Analysis'),
                    html.Div(
                    [
                        html.A(
                            html.Button("Go", id="learn-more-button"),
                            href="/covid19",
                        )
                    ],
                    className="one-half column",
                    id="button",
                ),
                    
                    ],
                    className="mini_container",
                    ),
            html.Div(
                    [
                    html.H6("Covid19 New"),
                    html.P("Covid 19 India Statewise trends and more"),
                    html.Div(
                    [
                        html.A(
                            html.Button("Go", id="learn-more-button"),
                            href="/common",
                        )
                    ],
                    className="one-half column",
                    id="button",
                ),
                    ],
                    className="mini_container",
                    ),
                    
            ],
                    className="row container-display",)
                    
])

 
covid_layout = helper.covid_layout
common_layout = helper.common_layout
    
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
    elif pathname == "/common":
        return common_layout
    else:
        return layout_index


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)
    
if __name__ == '__main__':
    app.run_server()
