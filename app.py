import os

# Dash stuff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
# Pandas 
import pandas as pd
# Flask errata? jesus
from flask import send_from_directory

### Get CSV
# !index!, Date, Image\ URL, Lat, Long, Object, Material, Brand, Other 
litter = pd.read_csv("./clean.csv")
brands_litter = pd.read_csv("./brands_clean.csv")
material_litter = pd.read_csv("./material_clean.csv")
object_litter = pd.read_csv("./object_clean.csv")


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.LUMEN]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### Info
app.title = 'Pasadena Litter Club'

server = app.server

### Style variables
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 2rem",
    "background-color": "#77efff",
    "overflow-y": "scroll"
}
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem"
}

### Figures
# Map
map_fig = px.scatter_geo(litter,
            lat="Lat", lon="Long",
            color="Tags",
            color_continuous_scale=px.colors.diverging.Picnic,
            projection="equirectangular",
            width=None, height=None)
# Mapbox?
map_key = os.environ["MAPBOX_KEY"]
px.set_mapbox_access_token(map_key)
mapbox_fig = px.scatter_mapbox(litter,
                                lat="Lat",
                                lon="Long",
                                color_continuous_scale=px.colors.cyclical.Edge,
                                zoom=18,
                                size_max=16,
                                mapbox_style="streets",
                                labels=litter.Brand,
                                center={"lat":34.15884884293918, "lon":-118.08851355364331},
                                hover_name="Tags",
                                width=None, height=None).update_layout(
                                    autosize=True, height=800
                                )

# Treemap (boxy thingie)
tree_fig = px.treemap(
    litter, 
        path=['Object', 'Material'],
        values='Brand_id',
        color='Material').update_layout(
            autosize=True, height=800
        )

# Pie charts
brands_litter.loc[brands_litter['amount'] < 3, 'brand'] = 'random brands'
material_litter.loc[material_litter['amount'] < 10, 'material'] = 'random materials'
object_litter.loc[object_litter['amount'] < 10, 'object'] = 'random objects'

brand_pie = px.pie(brands_litter, values='amount', names='brand', title='Most Littered Brands',
                    color_discrete_sequence=px.colors.sequential.RdBu).update_layout(autosize=True)
obj_pie = px.pie(object_litter, values='amount', names='object', title='Most Common Objects Littered',
                    color_discrete_sequence=px.colors.sequential.Rainbow).update_layout(autosize=True)
mat_pie = px.pie(material_litter, values='amount', names='material', title='Most Common Litter Materials',
                    color_discrete_sequence=px.colors.sequential.Turbo).update_layout(autosize=True)

# Navigation sidebar
sidebar = html.Div(
    [
        html.H2("Water & Litter", className="display-4"),
        html.Hr(),
        html.P(
            '''
            This website is a interactive presentation of litter 
            near and around the Eaton Wash in Pasadena— the very same wash that
            runs into the LA river and comes from 
            our mountains and eventually feeds into our oceans.
            ''', className="lead"
        ),
        html.Hr(),
        html.P(
            ''' 
            Data was collected over the course of 31~ days.
            There was no emphasis on any part of any parks as many
            pollutants from litter seep into the ground,
            all ground area was attempted to be covered except
            for areas that were inaccesible.
            '''
        ),
        html.P(
            '''
            Data is organised into three categories: object such as 'cigarettebutt',
            material such as 'celluloseacetate', and brand such as 'Marlboro'. Most
            detritus has no brand, so it won't be labelled with any brand when hovered over on
            the map.
            '''
        ),
        html.P(
            '''
            The data is not perfect, there are mistakes, but an honest attempt was made
            in labelling the appropriate designations for all 1200+ entries.
            '''
        ),
        html.P(
            '''
            The map is centered on the Gwinn and Eaton Sunnyslope parks,
            data is also from the Ernest E. Debs Regional Park area
            around 11.82 km (7.35 mi) away, which you can scroll to if you zoom out
            and feel like exhausting your scroll wheel :P
            '''
        ),
        html.Hr(),
        dbc.Nav(
            [
                html.Br(),
                dbc.NavLink("Contact your Representative to support the Green New Deal!", 
                            href="https://www.house.gov/representatives/find-your-representative", active="exact"),
                html.Br(),
                dbc.NavLink("Donate to a clean water charity!", 
                            href="https://www.charitywater.org/donate", active="exact")
            ],
            vertical=False,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

map_area = dbc.Container(
    html.Div([
        html.P('''
            The sheer quantity of trash was suprising. The amount of trash numbered at around 1,210 individual pieces.
            Pasadena is a nice city but despite this the plague of litter is still a problem in some public spaces!
        '''),
        html.P('''
            The worst hotspots for trash were ironically where the no-smoking signs were. The cluster in the eastern part of
            Eaton Sunnyslope had a 100+ cigarette butts, new to unbelievably old—the paper had already disappeared and all
            that was left was a husk of cellulose acetate. There were even a few pods for vapes scattered randomly around
            the parks.
        '''),
        html.Hr()
    ])
)

cell_ace = dbc.Container(
    dbc.Row([
        dbc.Col(
            [
                html.P('''Cellulose acetate (plastic fibers) is bad news! 
                It's a plastic used as a filter for cigarettes, and in the process of being a filter
                it absorbs all the bad chemicals such as nicotine and heavy metals from the cigarette. When it's
                thrown onto the ground as it is commonly is, those same bad chemicals leach into the ground
                polluting the soil and surrounding waters!''')
            ]
        ),
        dbc.Col(
            [
                html.Img(src='assets/ac_3d.png', className='img-fluid')
            ]
        )
    ])
)

pie_area = dbc.Container(
    html.Div([
        dcc.Graph(figure=brand_pie),
        html.Br(),
        dbc.Row([
            dbc.Col(
                [
                    html.Img(src='assets/ssweets.jpg', className='img-fluid')
                ]
            ),
            dbc.Col(
                [
                    html.P('''
                    SwisherSweets is the absolute bain of my existence, the packaging (torn-off tops and sometimes the whole
                    thing) seemed to spawn sponteanously in these parks! I also found some cigarettes near the bus
                    stop that had Traditional Chinese on it, I wondered what brand it was—interesting international litter!
                    I expected far more Starbucks branded goods, the idea of walking in the park and drinking a latte I guess
                    was my idea, but it was a happy surprise to never see that kind of trash.
                    Marlboro was assumed for some entries so it's not as significant as it may look at first.
                    '''),
                    html.Hr(),
                    html.P('''
                    The nerf darts were also an interesting find. They all seemed the same size, so presumably they're
                    from the same super-cool nerf gun.
                    '''),
                    html.P('''
                    Finding the old rubber flags from the city were kinda funny, there's always something missed after doing
                    significant construction or parks-and-rec work!
                    ''')
                ]
            )
        ]),
        dcc.Graph(figure=mat_pie),
    html.Div([cell_ace]),
        dcc.Graph(figure=obj_pie),
        html.P('''
        Wrappers were quite popular, or at least the torn pieces off the top of wrappers. It seems
        many people likely threw away 80% of the wrapper but the last torn piece got lost easily.
        Or at least that's what I tell myself..
        ''')
    ])
)

tree_area = dbc.Container(
    html.P('''
        If the data was cleaner and not absolutely jumbled this tree graph would be
        an excellent visualizer...I still added it to the site cause it simply looks cool
        even if it's wonky!
    '''),
)

# Main body
content = html.Div([
    html.Div(id="display-value"),
    html.H1("Welcome!"),
    dcc.Graph(figure=mapbox_fig),
    html.Div([map_area]),
    # Tree graph to show the material most found
    html.Div([pie_area]),
    html.Hr(),
    html.Div([tree_area]),
        dcc.Graph(figure=tree_fig)
    # Show Cellulose Acetate info
    #html.H4("See which park had what!"),
    #    dcc.Graph(figure=sunburst_fig)
    ], 
    style=CONTENT_STYLE
)

app.layout = html.Div([html.Div(id="loading"),dcc.Location(id="url"), sidebar, content])

#@app.callback(dash.dependencies.Output('display-value', 'children'),
#              [dash.dependencies.Input('dropdown', 'value')])
app.callback(dash.dependencies.Output('display-value', 'children'))
def display_value(value):
    if value == "/":
        return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=False)
