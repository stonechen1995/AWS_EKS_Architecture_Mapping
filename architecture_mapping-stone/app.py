# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# see https://plotly.com/python/px-arguments/ for more options

from dash import Dash, dcc, html, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from DashComponents import header, dropdown, graph, button
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url, load_figure_template
from mapping import Mapping
import pandas as pd

path = 'EKS-1million.csv'
map = Mapping(path)
map.map()

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

selec_input = dbc.Card([dropdown,button], body=True)
charts      = dbc.Card([graph], body = True)
app.layout = dbc.Container(
       [
           header,
           dbc.Row(
               [dbc.Col(ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.FLATLY}), width=2,),
               dbc.Col([selec_input], width =6),
               dbc.Col([charts],width =10),],),
        ],
        fluid = True,
        className = "dbc",)


@app.callback(
    Output("accountId-dropdown", "options"),
    Input("accountId-dropdown", "value"),
    prevent_initial_call=False
)
def account_dropdown_populater(account_id):
    print("\ncallback @ account_dropdown_populater")
    return map.find_name_of_children_of([])


@app.callback(
    Output("node-dropdown", "options"),
    Input("accountId-dropdown", "value"),
    prevent_initial_call=True
)
def node_dropdown_populater(account_id):
    print("\ncallback @ node_dropdown_populater")
    return map.find_name_of_children_of([account_id])


@app.callback(
    Output("node-dropdown", "value"),
    Output("pod-dropdown", "value"),
    Input("accountId-dropdown", "value"),
    Input("node-dropdown", "value"),
    prevent_initial_call=True
)
def clear_Dropdown_Input_Value_When_Upper_Input_Cleared(account_id, node_name):
    print("\ncallback @ clear_Dropdown_Input_Value_When_Upper_Input_Cleared")
    if account_id == None or node_name == None:
        print("clear dropdown inputs")
        return None, None
    else: 
        print("no updates")
        return dash.no_update

@app.callback(
    Output("pod-dropdown", "options"),
    State("accountId-dropdown", "value"),
    Input("node-dropdown", "value"),
    prevent_initial_call=True
)
def pod_dropdown_populater(account_id, node_name):
    print("\ncallback @ pod_dropdown_populater")
    if (node_name != None):
        print("output dropdown list")
        return map.find_name_of_children_of([account_id,node_name])
    else:
        print("no updates")
        return dash.no_update


@app.callback(
              Output("architecture_figure", "figure"),
              State("accountId-dropdown", "value"),
              State("node-dropdown", "value"),
              State("pod-dropdown","value"),
              Input('btn-nclicks-1', 'n_clicks'),
              prevent_initial_call=True 
)
def graph_displayer(account_id, node_name, pod_name, no_of_clicks):
    print("\ncallback @ graph_displayer")
    print(f"account_id = {account_id}")
    print(f"node_name = {node_name}")
    print(f"pod_name = {pod_name}")
    print(f"no_of_clicks = {no_of_clicks}")
    if no_of_clicks > 0:
        if account_id != None and node_name != None and pod_name != None:
            print(f"show components under {[account_id,node_name,pod_name]}")
            return map.graphLayerOf([account_id,node_name,pod_name], 80)
        elif account_id != None and node_name != None and pod_name == None:
            print(f"show components under {[account_id,node_name,pod_name]}")
            return map.graphLayerOf([account_id,node_name], 80)
        elif account_id != None and node_name == None and pod_name == None:
            print(f"show components under {[account_id,node_name,pod_name]}")
            return map.graphLayerOf([account_id], 80)
        elif account_id == None and node_name == None and pod_name == None:
            print(f"show components under {[account_id,node_name,pod_name]}")
            return map.graphLayerOf([], 80)
        else:
            print("input invalid, no updates")
            return dash.no_update
    else: 
        print("No Click, no updates")
        return dash.no_update




if __name__ == '__main__':
    app.run_server(debug=True)
