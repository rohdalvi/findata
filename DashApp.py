import dash
import dash_core_components as dcc
import dash_html_components as html 
from getData import databaseSetUp
import sqlite3
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

def acquireData():
    cur, conn = databaseSetUp('AVdata.db')
    cur.execute("SELECT time FROM stockData")
    x = cur.fetchall()

    cur.execute("SELECT closingPrice FROM stockData")
    y = cur.fetchall()

    return x,y

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='Hello Dash', 
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
