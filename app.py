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


#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.CERULEAN]

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
    "width": "22rem",
    "padding": "2rem 2rem",
    "background-color": "#44efff"
}
CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem"
}

### Figures
# Map
map_fig = px.scatter_geo(litter,
            lat="Lat", lon="Long",
            color="Object",
            color_continuous_scale=px.colors.diverging.Picnic,
            projection="equirectangular",
            width=None, height=None)
# Mapbox?
map_key = os.environ["MAPBOX_KEY"]
px.set_mapbox_access_token(map_key)
mapbox_fig = px.scatter_mapbox(litter,
                                lat="Lat",
                                lon="Long",
                                color="Object",
                                color_continuous_scale=px.colors.cyclical.Edge,
                                zoom=18,
                                size_max=16,
                                mapbox_style="basic",
                                labels=litter.Brand,
                                center={"lat":34.15884884293918, "lon":-118.08851355364331},
                                hover_name="Brand",
                                width=None, height=None).update_layout(
                                    autosize=True, height=800
                                )

# Treemap (boxy thingie)
tree_fig = px.treemap(
    litter, 
        path=['Object', 'Material'],
        values='Brand_id').update_layout(
            autosize=True, height=800
        )

# Sunburst
sunburst_fig = px.sunburst(
    litter,
    names='Object',
    parents='Material',
    values='Brand_id'
)

# Navigation sidebar
sidebar = html.Div(
    [
        html.H2("Water & Litter", className="display-4"),
        html.Hr(),
        html.P(
            '''This website is a interactive presentation of litter 
            near and around the Eaton Wash in Pasadena— the very same wash that
            runs into the LA river and comes from 
            our mountains and eventually feeds into our oceans.''', className="lead"
        ),
        html.Hr(),
        html.P(

        ),
        dbc.Nav(
            [
                html.Br(),
                dbc.NavLink("Contact your Rep!", href="https://www.house.gov/representatives/find-your-representative", active="exact"),
                html.Br(),
                dbc.NavLink("Water Donation", href="https://www.charitywater.org/donate", active="exact")
            ],
            vertical=False,
            pills=False,
        ),
    ],
    style=SIDEBAR_STYLE,
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

# Main body
content = html.Div([
    html.Div(id="display-value"),
    html.H1("Welcome!"),
    dcc.Graph(figure=mapbox_fig),
    # Tree graph to show the material most found
    html.H3("See which material was found the most!"),
        dcc.Graph(figure=tree_fig),
    # Show Cellulose Acetate info
    html.Div([cell_ace]),
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
