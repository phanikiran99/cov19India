# -*- coding: utf-8 -*-
# dict of state names to shortcuts
import dash_core_components as dcc
import dash_html_components as html
import plots
import geo
import base64
import sqlite3

def retriveArticlesList():
    conn = None
    try:
        conn = sqlite3.connect('static/entries.db')
    except:
        print ('unable to connect')
    cur = conn.cursor()
    cur.execute('select * from entry_list')
    rows = cur.fetchall()
    article_list = []
    for row in rows:
        article_list.append(row)   
    
    return article_list

dict = {'an': 'Andaman & Nicobar Island',
 'ap': 'Andhra Pradesh',
 'ar': 'Arunanchal Pradesh',
 'as': 'Assam',
 'br': 'Bihar',
 'ch': 'Chandigarh',
 'ct': 'Chhattisgarh',
 'dd': 'Dadara & Nagar Havelli',
 'dl': 'NCT of Delhi',
 'dn': 'Daman & Diu',
 'ga': 'Goa',
 'gj': 'Gujarat',
 'hp': 'Himachal Pradesh',
 'hr': 'Haryana',
 'jh': 'Jharkhand',
 'jk': 'Jammu & Kashmir',
 'ka': 'Karnataka',
 'kl': 'Kerala',
 'la': '',
 'ld': 'Lakshadweep',
 'mh': 'Maharashtra',
 'ml': 'Meghalaya',
 'mn': 'Manipur',
 'mp': 'Madhya Pradesh',
 'mz': 'Mizoram',
 'nl': 'Nagaland',
 'or': 'Odisha',
 'pb': 'Puducherry',
 'py': 'Punjab',
 'rj': 'Rajasthan',
 'sk': 'Sikkim',
 'tg': 'Telangana',
 'tn': 'Tamil Nadu',
 'tr': 'Tripura',
 'tt': '',
 'up': 'Uttar Pradesh',
 'ut': 'Uttarakhand',
 'wb': 'West Bengal'}


#geo.saveImages();

fig  = plots.fig  # trend line
fig2 = plots.fig2 # doubling rate
fig3 = plots.fig3

rec_filename = 'static/recovery.png' # replace with your own image
encoded_image_rec = base64.b64encode(open(rec_filename, 'rb').read())


act_filename = 'static/active.png' # replace with your own image
encoded_image_act = base64.b64encode(open(act_filename, 'rb').read())    

states_options = [{'label':i[1],'value':i[0]} for i in dict.items()]

covid_layout= html.Div(children=[
        html.Div('Covid19 India EDA Short analysis on How India is dealing with Covid19',className='row container-display pretty_container col-md-12 container-fluid'),
        html.Div([html.H3('State',className='pretty_container col-md-4'),
                  html.Div([dcc.Dropdown(options=states_options,multi=True,value='ap')]
                ,className='pretty_container col-md-8'),]
            ,className='row container-display'),
        html.Div([html.Div([dcc.Graph(id='cov1',figure=fig)],className='pretty_container container-fluid col-md-6'),
                  html.Div([dcc.Graph(id='c0v2',figure=fig3)],className='pretty_container container-fluid col-md-6')],
        className='row container-display'),
    
    html.Div([
    html.H2("Doubling Rate of Cases"),
    dcc.Graph(
        id='Cov2',
        figure=fig2
    ),
            ],
            className='pretty_container'),
    html.Div([
    html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image_act.decode())),
    ],
    className='pretty_container col-md-4 container-fluid'),
    html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image_rec.decode())),
            ],
            className='pretty_container col-md-4 container-fluid'),
            ],
    className='row container-display'),
    html.A('Code on Github', href='https://github.com/phanikiran99/cov19India'),
    html.Br(),
    html.A('Data Source', href='covid19india.org'),
    ]
)




