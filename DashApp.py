import dash
import dash_core_components as dcc
import dash_html_components as html 
from getData import databaseSetUp
import sqlite3
import requests
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


cur, conn = databaseSetUp('AVdata.db')
cur.execute("SELECT time FROM stockData")
x_data = cur.fetchall()
x1 = []
for i in x_data:
    x1.append(i[0])

cur.execute("SELECT closingPrice FROM stockData")
y_data = cur.fetchall()
y1 = []
for i in y_data:
    y1.append(i[0])

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='stockData', 
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Built with Dash and Python.', style={
        'textAlign': 'center',
        'color': colors['text'],
    }),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                go.Scatter(
                    x=x1,
                    y=y1,
                    mode = 'markers+lines',
                    marker = dict(
                        color= colors['text']
                    )
                    
                ) 
            ],
            'layout': go.Layout(
                title= 'AAPL Price Visualization',
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background'], 
                font= {
                    'color': colors['text']
                }
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
