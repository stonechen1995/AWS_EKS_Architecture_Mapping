from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
# from mapping import Mapping
# from app import map
import pandas as pd

# path = 'EKS-1million.csv'
# map = Mapping(path)
# map.map()


header = html.H4("EKS Architecture Map",
             className="bg-primary text-white p-3 mb-2 text-center")

button = html.Div([
    html.Button('Boom', id='btn-nclicks-1', n_clicks=0),
    html.Div(id='generate-map')
])

dropdown = html.Div([
        dbc.Label("Please select account"),
         dcc.Dropdown(
           id = "accountId-dropdown",
           # options=[{"label": str(i), "value": i} for i in map.find_name_of_children_of([])],
           multi = False,),
        dbc.Label("Please select instance"),
         dcc.Dropdown(
           id = "node-dropdown",
           multi = False,),
        dbc.Label("Please select pod"),
         dcc.Dropdown(
           id = "pod-dropdown",
           multi = False,),
        ],
        className="mb-4",)

## loads custom architecture map for the specified account
graph = html.Div(
        [dcc.Graph(
           id = "architecture_figure",
           style={'width': '160vh', 'height': '80vh','display': 'inline-block'})],
           className="m-4")
