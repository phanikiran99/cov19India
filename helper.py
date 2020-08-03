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
 'wb': 'West Bengal',
 'un': 'Unknown'}


#geo.saveImages();

fig  = plots.fig  # trend line
fig2 = plots.fig2 # doubling rate
fig3 = plots.fig3
fig4 = plots.fig4

rec_filename = 'static/recovery.png' # replace with your own image
encoded_image_rec = base64.b64encode(open(rec_filename, 'rb').read())


act_filename = 'static/active.png' # replace with your own image
encoded_image_act = base64.b64encode(open(act_filename, 'rb').read())    

states_options = [{'label':i[1],'value':i[0]} for i in dict.items()]

def commonLayout(layoutTitle='Title',numFilters=2,filter1Name='Filter1',
                 filter2Name='Filter2',
                 filter1Options=[{}], filter2Options=[{}], figList=[]):
    """
    Parameters : layoutTitle = Title of the page
    numfilters = Total number of filters - supports two filters
    filter'n'Name = name of filters
    filter'n'Options = options for dropdown values
    figlist - list of lists with id, fig object, Text description of figure
    """
    # prepare for filter area
    filterArea  =  html.Div([html.H5(filter1Name,className='col-md-2'),
                  html.Div([dcc.Dropdown(options=filter1Options,multi=True,value='ap')]
                ,className='col-md-4'),
                html.H5(filter2Name,className='col-md-2'),
                  html.Div([dcc.Dropdown(options=filter2Options,multi=True,value='ap')]
                ,className='col-md-4'),]
            ,className='row container-display pretty_container')       
    # prepare for plots
    figureArea = []
    for i,fig in enumerate(figList):
        if i%2 == 0:
            figureArea.append(html.Div([html.Div([dcc.Graph(id=fig[0], figure=fig[1])], className='pretty_container col-md-10'),
                                        html.Div([html.P(fig[2])], className='pretty_container col-md-2 text-left')], 
                                        className='row container-display'))
        else:
            figureArea.append(html.Div([html.Div([html.P(fig[2])], className='pretty_container col-md-2 text-right'),
                                        html.Div([dcc.Graph(id=fig[0], figure=fig[1])], className='pretty_container col-md-10'),
                                        ], 
                                        className='row container-display'))
            
    updatedLayout = html.Div(children=[
        html.Div(html.H4(layoutTitle),className='row pretty_container col-md-12 container-fluid center'),
        filterArea,
        html.Div(figureArea),]
        )
    
    return updatedLayout



common_layout = commonLayout(layoutTitle='Covid19 India EDA Short analysis on How India is dealing with Covid19',numFilters=2,filter1Name='State',
                 filter2Name='Filter2',
                 filter1Options=states_options,
                 filter2Options=[{'label':'1','value':'1'},{'label':'2','value':'2'}], 
                 figList=[['test',fig,plots.figText],['test2',fig4,plots.fig4Text]])

covid_layout= html.Div(children=[
        html.Div('Covid19 India EDA Short analysis on How India is dealing with Covid19',className='row pretty_container col-md-12 container-fluid'),
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


covtab_layout = html.Div(html.Iframe(src="https://public.tableau.com/views/Covid19InIndia/Indiatotal?:language=en-GB&:display_count=y&publish=yes&:origin=viz_share_link:showVizHome=no&:embed=true showVizHome=no&:embed=true"
                                     ,width='100%', height="655"
                                     ),className='pretty_container col-md-12 container-fluid')