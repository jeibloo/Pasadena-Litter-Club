import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# Bootstrap errata
import dash_bootstrap_components as dbc
# Plotly express errata
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#36beff"
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

# Navigation sidebar
sidebar = html.Div(
    [
        html.H2("Water's Water", className="display-4"),
        html.Hr(),
        html.P(
            "Cool links for cool kidz", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                html.Br(),
                dbc.NavLink("Donation", href="/Donation", active="exact"),
                html.Br(),
                dbc.NavLink("Contact Your Rep", href="/contact", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Main body
content = html.Div([
    dcc.Dropdown(
        id="page-content", 
        options=[{'label': i, 'value': i} for i in ['Gwinn Park', 'Arroyo Seco']],
        value='LA'
        ),
    html.Div(id="display-value")
    ], 
    style=CONTENT_STYLE
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=False)
