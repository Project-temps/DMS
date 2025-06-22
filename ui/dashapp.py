"""Dash app for visualizing environmental data inside Django."""

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
import logging
from django_plotly_dash import DjangoDash
from data_management.data_loader import load_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Initializing Dash app")


# Load hourly aggregated data
logger.info("Loading data for dashapp")
try:
    df = load_data('hourly_merged_sensor_data.csv')
    logger.info("Data loaded successfully with shape %s", df.shape)
except FileNotFoundError as e:
    logger.exception("Data file could not be loaded: %s", e)
    df = pd.DataFrame()
    
# from flask_cors import CORS

current_directory = os.path.dirname(os.path.abspath(__file__))


app = DjangoDash('dashapp')
# server = app.server  # the Flask app
# CORS(server, resources={r"/*": {"origins": "*"}})
# app.run(port=8000)

# data_path = os.path.join(current_directory, 'train_cleaned_dataset_modified.csv')

# df = pd.read_csv(data_path)

feature_groups = {
    'CH4': ['ch4'],
    'CO2': ['co2'],
    'NH3': ['nh3'],
    'Temperature': ['temperature'],
    'Humidity': ['humidity'],
    'Wind': ['wind_ns', 'wind_ew']
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
    fig = px.line(df, x='datetime', y=selected_features, title=f'Time Series for Selected Features')
    return fig


if __name__ == '__main__':
    app.run_server(port=8000, debug=False)
