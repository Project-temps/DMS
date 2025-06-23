"""Dash app for visualizing environmental data inside Django."""

import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import os
import logging
from django_plotly_dash import DjangoDash
from data_management.data_loader import load_data
from data_management.calculate_thi import add_thi_column

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Initializing Dash app")


# Load hourly aggregated data
logger.info("Loading data for dashapp")
try:
    df_germany = load_data('hourly_merged_sensor_data.csv', country='Germany')
    df_poland = load_data('hourly_merged_sensor_data.csv', country='Poland')

    # ensure datetime columns are parsed
    df_germany['datetime'] = pd.to_datetime(df_germany['datetime'], utc=True)
    df_poland['datetime'] = pd.to_datetime(df_poland['datetime'], utc=True)

    # Append THI column using shared helper
    df_germany = add_thi_column(df_germany)
    df_poland = add_thi_column(df_poland)

    dataframes = {
        'Germany': df_germany,
        'Poland': df_poland,
    }
    min_date = min(df_germany['datetime'].min(), df_poland['datetime'].min())
    max_date = max(df_germany['datetime'].max(), df_poland['datetime'].max())
    logger.info(
        "Data loaded successfully: DE %s, PL %s",
        df_germany.shape,
        df_poland.shape,
    )
except FileNotFoundError as e:
    logger.exception("Data file could not be loaded: %s", e)
    dataframes = {'Germany': pd.DataFrame(), 'Poland': pd.DataFrame()}
    min_date = max_date = None
    
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
        ], style={'width': '50%', 'padding': '10px'}),
        html.Div([
            dcc.Checklist(
                id='dataset-toggle',
                options=[{'label': 'Germany', 'value': 'Germany'},
                         {'label': 'Poland', 'value': 'Poland'}],
                value=['Germany', 'Poland'],
                labelStyle={'margin-right': '10px'}
            )
        ], style={'padding': '10px'}),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format='YYYY-MM-DD HH:mm'
        ),
        html.Button('Export CSV', id='export-button', n_clicks=0, style={'margin': '10px'}),
        dcc.Download(id='download-data'),
        dcc.Graph(
            id='feature-graph',
            style={'height': '70vh', 'width': '100%'},
            config={'responsive': True}
        ),
    ], style={'margin-bottom': '50px'}),

    html.Div(id='thi-section', children=[
        html.H2("THI Index", style={'textAlign': 'center'}),
        dcc.Graph(
            id='thi-graph',
            style={'height': '70vh', 'width': '100%'},
            config={'responsive': True}
        ),
        html.Button('Export THI CSV', id='export-thi-button', n_clicks=0, style={'margin': '10px'}),
        dcc.Download(id='download-thi-data'),
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
        Input('dataset-toggle', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
    ]
)
def update_graph(selected_tab, selected_features, selected_datasets, start_date, end_date):
    if not selected_features or not selected_datasets:
        return dash.no_update

    start_ts = pd.to_datetime(start_date, utc=True)
    end_ts = pd.to_datetime(end_date, utc=True)

    fig = go.Figure()
    for dataset in selected_datasets:
        df = dataframes.get(dataset, pd.DataFrame())
        if df.empty:
            continue
        mask = (df['datetime'] >= start_ts) & (df['datetime'] <= end_ts)
        filtered = df.loc[mask]
        for feature in selected_features:
            if feature in filtered.columns:
                fig.add_trace(
                    go.Scatter(
                        x=filtered['datetime'],
                        y=filtered[feature],
                        mode='lines',
                        name=f'{dataset} {feature}',
                    )
                )

    fig.update_layout(title='Time Series for Selected Features', autosize=True)
    return fig


@app.callback(
    Output('download-data', 'data'),
    Input('export-button', 'n_clicks'),
    State('feature-dropdown', 'value'),
    State('dataset-toggle', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'),
    prevent_initial_call=True,
)
def export_data(n_clicks, selected_features, selected_datasets, start_date, end_date):
    if not selected_features or not selected_datasets:
        return dash.no_update

    start_ts = pd.to_datetime(start_date, utc=True)
    end_ts = pd.to_datetime(end_date, utc=True)

    frames = []
    for dataset in selected_datasets:
        df = dataframes.get(dataset, pd.DataFrame())
        if df.empty:
            continue
        mask = (df['datetime'] >= start_ts) & (df['datetime'] <= end_ts)
        filtered = df.loc[mask, ['datetime'] + selected_features].copy()
        filtered['dataset'] = dataset
        frames.append(filtered)

    if not frames:
        return dash.no_update

    result = pd.concat(frames)
    return dcc.send_data_frame(result.to_csv, 'export.csv', index=False)


@app.callback(
    Output('thi-graph', 'figure'),
    [
        Input('dataset-toggle', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
    ]
)
def update_thi_graph(selected_datasets, start_date, end_date):
    if not selected_datasets:
        return dash.no_update

    start_ts = pd.to_datetime(start_date, utc=True)
    end_ts = pd.to_datetime(end_date, utc=True)

    fig = go.Figure()
    for dataset in selected_datasets:
        df = dataframes.get(dataset, pd.DataFrame())
        if df.empty:
            continue
        mask = (df['datetime'] >= start_ts) & (df['datetime'] <= end_ts)
        filtered = df.loc[mask]
        if 'thi' in filtered.columns:
            fig.add_trace(
                go.Scatter(
                    x=filtered['datetime'],
                    y=filtered['thi'],
                    mode='lines',
                    name=f'{dataset} THI',
                )
            )

    fig.update_layout(title='Temperature-Humidity Index', autosize=True)
    return fig


@app.callback(
    Output('download-thi-data', 'data'),
    Input('export-thi-button', 'n_clicks'),
    State('dataset-toggle', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'),
    prevent_initial_call=True,
)
def export_thi_data(n_clicks, selected_datasets, start_date, end_date):
    if not selected_datasets:
        return dash.no_update

    start_ts = pd.to_datetime(start_date, utc=True)
    end_ts = pd.to_datetime(end_date, utc=True)

    frames = []
    for dataset in selected_datasets:
        df = dataframes.get(dataset, pd.DataFrame())
        if df.empty:
            continue
        mask = (df['datetime'] >= start_ts) & (df['datetime'] <= end_ts)
        filtered = df.loc[mask, ['datetime', 'thi']].copy()
        filtered['dataset'] = dataset
        frames.append(filtered)

    if not frames:
        return dash.no_update

    result = pd.concat(frames)
    return dcc.send_data_frame(result.to_csv, 'thi_export.csv', index=False)


if __name__ == '__main__':
    app.run_server(port=8000, debug=False)
