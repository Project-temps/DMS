<<<<<<< HEAD
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os
from django_plotly_dash import DjangoDash
from data_management.data_loader import load_data
from data_processing.prediction import make_prediction


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

    html.Div(id='prediction-section', children=[
        html.H2("Prediction", style={'textAlign': 'center'}),
        html.Div([
            html.Button('Predict', id='predict-button', n_clicks=0),
            html.Div(id='prediction-output', style={'textAlign': 'center'})
        ], style={'textAlign': 'center'}),
    ], style={'background-color': '#f7f7f7', 'padding': '20px', 'border-top': '2px solid #ccc'}),
], style={'height': '100vh', 'width': '100%'})

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

@app.callback(
    Output('prediction-output', 'children'),
    [Input('predict-button', 'n_clicks')],
    prevent_initial_call=True
)
def update_output(n_clicks):
    if n_clicks > 0:
        fig = make_prediction()
        return dcc.Graph(figure=fig)
    return "Click Predict to get the predictions."

if __name__ == '__main__':
    app.run_server(port=8000, debug=False)
=======
import os
import glob
import pandas as pd
from dash import dcc, html, Input, Output
# from dash_extensions.snippets import send_data_frame
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash import dcc

# adjust this so it points at your repo’s data/processed
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

# load CSVs and tag by farm
all_files = glob.glob(os.path.join(DATA_DIR, '**', '*.csv'), recursive=True)
dfs = []
for f in all_files:
    farm = os.path.basename(f).split('_')[0]
    df = pd.read_csv(f, parse_dates=[0])
    df.rename(columns={df.columns[0]:'Date'}, inplace=True)
    df['Farm'] = farm
    dfs.append(df)
    # diagnostic output to confirm each CSV was loaded
    print(f"Loaded {f} with {len(df)} rows for farm {farm}")

df_all = pd.concat(dfs, ignore_index=True)
print(f"Concatenated {len(df_all)} total rows across {df_all['Farm'].nunique()} farms")
time_col = 'Date'
params = [c for c in df_all.columns if c not in ['Farm', time_col]]

app = DjangoDash("FarmTimeSeries")

app.layout = html.Div([
    html.H2("Farm Data Dashboard", style={'textAlign':'center'}),
    html.Div([
        html.Label("Farms:"),
        dcc.Checklist(
            id='farm-selector',
            options=[{'label':f,'value':f} for f in sorted(df_all.Farm.unique())],
            value=sorted(df_all.Farm.unique()),
            inline=True
        )
    ], style={'padding':'10px'}),

    html.Div([
        html.Label("Parameters:"),
        dcc.Dropdown(
            id='param-selector',
            options=[{'label':p,'value':p} for p in params],
            value=[params[0]],
            multi=True
        )
    ], style={'padding':'10px'}),

    html.Div([
        html.Label("Date range:"),
        dcc.DatePickerRange(
            id='date-range',
            start_date=df_all[time_col].min().date(),
            end_date=df_all[time_col].max().date()
        )
    ], style={'padding':'10px'}),

    dcc.Graph(id='time-series-graph'),

    html.Button("Export CSV", id='export-button'),
    dcc.Download(id='download-data')
])

@app.callback(
    Output('time-series-graph','figure'),
    Input('farm-selector','value'),
    Input('param-selector','value'),
    Input('date-range','start_date'),
    Input('date-range','end_date'),
)
def update_graph(farms, params_sel, start, end):
    if not farms or not params_sel:
        return {}
    dff = df_all[df_all.Farm.isin(farms)]
    dff = dff[(dff.Date>=start)&(dff.Date<=end)]
    fig = px.line(
        dff,
        x='Date',
        y=params_sel,
        color='Farm',
        title="Time Series Comparison"
    )
    return fig

@app.callback(
    Output('download-data','data'),
    Input('export-button','n_clicks'),
    Input('farm-selector','value'),
    Input('param-selector','value'),
    Input('date-range','start_date'),
    Input('date-range','end_date'),
)
def export_data(n, farms, params_sel, start, end):
    if not n:
        return
    dff = df_all[df_all.Farm.isin(farms)]
    dff = dff[(dff.Date>=start)&(dff.Date<=end)]
    cols = ['Farm','Date'] + params_sel
    return dcc.send_data_frame(dff[cols].to_csv, "exported.csv")

>>>>>>> origin/New_ui
