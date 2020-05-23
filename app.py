#dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plots
import geo
import base64


fig  = plots.fig  # trend line
fig2 = plots.fig2 # doubling rate

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

rec_filename = 'recovery.png' # replace with your own image

encoded_image_rec = base64.b64encode(open(rec_filename, 'rb').read())


act_filename = 'active.png' # replace with your own image
encoded_image_act = base64.b64encode(open(act_filename, 'rb').read())    
    
########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title="Phani-Writes"

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
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_act.decode())),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_rec.decode())),
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
