"""Dash app for visualizing environmental data inside Django."""

import dash
from dash import dcc, html, Input, Output, State
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
    df_germany = load_data('hourly_merged_sensor_data.csv', region='Germany')
    df_germany['region'] = 'Germany'
    df_poland = load_data('hourly_merged_sensor_data.csv', region='Poland')
    df_poland['region'] = 'Poland'
    df = pd.concat([df_germany, df_poland], ignore_index=True)
    df['datetime'] = pd.to_datetime(df['datetime'])
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
        html.Div([
            dcc.Checklist(
                id='dataset-checklist',
                options=[
                    {'label': 'Germany', 'value': 'Germany'},
                    {'label': 'Poland', 'value': 'Poland'}
                ],
                value=['Germany', 'Poland'],
                inline=True,
                style={'margin-right': '20px'}
            ),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['datetime'].min().date() if not df.empty else None,
                end_date=df['datetime'].max().date() if not df.empty else None,
            ),
            html.Button('Export CSV', id='export-btn', n_clicks=0, className='btn btn-primary ms-3')
        ], style={'display': 'flex', 'alignItems': 'center', 'padding': '10px'}),
        dcc.Tabs(id='feature-tabs', value='tab-CO2', children=[
            dcc.Tab(label=group, value=f'tab-{group}') for group in feature_groups.keys()
        ]),
        html.Div([
            dcc.Dropdown(id='feature-dropdown', multi=True)
        ], style={'width': '50%', 'padding': '20px'}),
        dcc.Graph(
            id='feature-graph',
            style={'height': '70vh', 'width': '100%'},
            config={'responsive': True}
        ),
        dcc.Download(id='download-data'),
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
    [
        Input('feature-tabs', 'value'),
        Input('feature-dropdown', 'value'),
        Input('dataset-checklist', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ]
)
def update_graph(selected_tab, selected_features, datasets, start_date, end_date):
    if not selected_features or not datasets:
        return dash.no_update

    dff = df[df['region'].isin(datasets)]
    if start_date and end_date:
        dff = dff[(dff['datetime'] >= start_date) & (dff['datetime'] <= end_date)]

    fig = px.line(
        dff,
        x='datetime',
        y=selected_features,
        color='region',
        title='Time Series for Selected Features'
    )
    fig.update_layout(autosize=True)
    return fig


@app.callback(
    Output('download-data', 'data'),
    Input('export-btn', 'n_clicks'),
    State('dataset-checklist', 'value'),
    State('feature-dropdown', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'),
    prevent_initial_call=True
)
def export_data(n_clicks, datasets, selected_features, start_date, end_date):
    if not datasets or not selected_features:
        return dash.no_update
    dff = df[df['region'].isin(datasets)]
    if start_date and end_date:
        dff = dff[(dff['datetime'] >= start_date) & (dff['datetime'] <= end_date)]
    dff = dff[['datetime', 'region'] + selected_features]
    return dcc.send_data_frame(dff.to_csv, 'environmental_data.csv')


if __name__ == '__main__':
    app.run_server(port=8000, debug=False)
