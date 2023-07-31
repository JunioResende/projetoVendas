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

@app.callback([
    Output('cityFig', 'figure'),
    Output('payFig', 'figure'),
    Output('incomePerProductFig', 'figure'),
], 
    [
        Input('checkCity', 'value'),
        Input('mainVariable', 'value')
        ])

def render_graphs(cities, mainVariable):
    
    # cities= ['Yangon', 'Mandelay']
    # mainVariable = 'gross income'
    
    operation = np.sum if mainVariable == 'gross income' else np.mean
    df_filtered = df_data[df_data['City'].isin(cities)]
    df_city = df_filtered.groupby('City')[mainVariable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[mainVariable].apply(operation).to_frame().reset_index()
    df_product_Income = df_filtered.groupby(['Product line','City'])[mainVariable].apply(operation).to_frame().reset_index()
    
    figCity = px.bar(df_city, x='City', y=mainVariable)
    figPayment = px.bar(df_payment, y='Payment', x=mainVariable, orientation='h')
    figProductIncome = px.bar(df_product_Income, x=mainVariable, y='Product line', color='City', orientation='h', barmode='group')
    
    figCity.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    figPayment.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    figProductIncome.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=400)
    
    return figCity, figPayment, figProductIncome




#=========Run Server=========
if __name__ == '__main__':
    app.run_server(port=8050, debug=True)