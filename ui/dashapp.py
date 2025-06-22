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

