"""Dash app for visualizing environmental data inside Django."""

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
from django_plotly_dash import DjangoDash
from data_management.data_loader import load_data


# Load data
try:
    df = load_data()
except FileNotFoundError as e:
    print(e)
    
# from flask_cors import CORS

current_directory = os.path.dirname(os.path.abspath(__file__))


app = DjangoDash('dashapp')
# server = app.server  # the Flask app
# CORS(server, resources={r"/*": {"origins": "*"}})
# app.run(port=8000)

# data_path = os.path.join(current_directory, 'train_cleaned_dataset_modified.csv')

# df = pd.read_csv(data_path)

feature_groups = {
    'CO2': ['CO2_w-out', 'CO2_s-out', 'CO2_n-out', 'CO2_e-out', 'CO2_n-in', 'CO2_m-in', 'CO2_m-in-up', 'CO2_s-in', 'CO2_w-in', 'CO2_e-in'],
    'NH3': ['NH3_w-out', 'NH3_s-out', 'NH3_n-out', 'NH3_e-out', 'NH3_n-in', 'NH3_m-in', 'NH3_m-in-up', 'NH3_s-in', 'NH3_w-in', 'NH3_e-in'],
    'CH4': ['CH4_w-out', 'CH4_s-out', 'CH4_n-out', 'CH4_e-out', 'CH4_n-in', 'CH4_m-in', 'CH4_m-in-up', 'CH4_s-in', 'CH4_w-in', 'CH4_e-in', 'CH4_in_mean', 'CH4_out_mean'],
    'Temperature': ['TEMP'],
    'Wind': ['Wind_dir', 'Wind_speed', 'Ver_w', 'Hor_w']
}



app.layout = html.Div([
    html.H1("Environmental Data Visualization Dashboard", style={'textAlign': 'center'}),

    html.Div(id='visualization-section', children=[
        html.P("Select a tab to visualize time series data.", style={'textAlign': 'center'}),
        dcc.Tabs(id='feature-tabs', value='tab-CO2', children=[
            dcc.Tab(label=group, value=f'tab-{group}') for group in feature_groups.keys()
        ]),
        html.Div([
            dcc.Dropdown(id='feature-dropdown', multi=True)
        ], style={'width': '50%', 'padding': '20px'}),
        dcc.Graph(id='feature-graph'),
    ], style={'margin-bottom': '50px'}),

], style={'width': '100%'})

@app.callback(
    Output('feature-dropdown', 'options'),
    [Input('feature-tabs', 'value')]
)
def set_features_options(selected_tab):
    group = selected_tab.split('-')[-1]
    return [{'label': i, 'value': i} for i in feature_groups[group]]

@app.callback(
    Output('feature-dropdown', 'value'),
    [Input('feature-dropdown', 'options')]
)
def set_features_value(available_options):
    return [option['value'] for option in available_options]

@app.callback(
    Output('feature-graph', 'figure'),
    [Input('feature-tabs', 'value'), Input('feature-dropdown', 'value')]
)
def update_graph(selected_tab, selected_features):
    if not selected_features:
        return dash.no_update
    fig = px.line(df, x='Date', y=selected_features, title=f'Time Series for Selected Features')
    return fig


if __name__ == '__main__':
    app.run_server(port=8000, debug=False)
