import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

# ========Tratamento de Dados =============
df_data = pd.read_csv('supermarket_sales.csv')
df_data['Date'] = pd.to_datetime(df_data['Date'])

# =========Layout===========
app.layout = html.Div(
    children=[
        html.H5('Cidades:'),
        dcc.Checklist(
                        df_data['City'].value_counts().index,
                        df_data['City'].value_counts().index,
                        id='checkCity'
                        ),
        
        html.H5('Variavel de analise'),
        dcc.RadioItems(
            ['gross income', 'Rating'], 
            'gross income', 
            id='mainVariable'
            ),
        
        dcc.Graph(id='cityFig'),
        dcc.Graph(id='payFig'),
        dcc.Graph(id='incomePerProductFig'),
    ]
)

# =========Callbacks========





#=========Run Server=========
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)