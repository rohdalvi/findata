import dash
import dash_core_components as dcc
import dash_html_components as html 
from getData import databaseSetUp, getAVdata, createDatabase
import sqlite3
import requests
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#002A38',
    'text': '#00CED1'  
}


cur, conn = databaseSetUp('AVdata.db')
cur.execute("SELECT time FROM AAPL_Table")
x_data = cur.fetchall()
x1 = []
for i in x_data:
    x1.append(i[0])

cur.execute("SELECT closingPrice FROM AAPL_Table")
y_data = cur.fetchall()
y1 = []
print("here")
for i in y_data:
    y1.append(i[0])

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='stockData', 
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div([
        html.Div([
            html.Div(children='Built with Dash and Python.', style={
                'textAlign': 'center',
                'color': colors['text'],
            }),
        ])
    ], className='row'),

    html.Div([
        html.Div([
            html.Div(dcc.Input(id='input-box', type='text')),
            html.Button('Submit', id='button'),
            html.Div(id='output-container-button', children='Enter a value and press submit')
        # html.Div(children=[
        #     dcc.Input(id='my-id', value='initial value', type='text', style = {
        #     'textAlign': 'center',
        #     'background-color': '#FFF8DC',
        # }, className = 'one column offset-by-one column'), 
        # html.Button('Submit', id='button')    
    ], className='row'),

    html.Div([
        html.Div(id='my-div', style = {
            'textAlign': 'center',
            'color' : colors['text'],
            'fontSize' : 24 
            }
            )
        ]),

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
                    plot_bgcolor= colors['background'],
                    paper_bgcolor= colors['background'], 
                    font= {
                        'color': colors['text']
                    },
                    xaxis=dict(
                        gridcolor= '#459894'
                    ),
                    yaxis=dict(
                        gridcolor= '#459894'
                    )
                )
            }
        )
     ], className = "row")

])

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')]
)

def update_graph_src(n_clicks, value):
    print(value)
    cur, conn = databaseSetUp('AVdata.db')
    data = getAVdata(value, "60min")
    name = value + "_Table"
    createDatabase(name, data, cur, conn)
    cur.execute("SELECT time FROM %s" % (name,))
    x_data = cur.fetchall()
    x1 = []
    for i in x_data:
        x1.append(i[0])

    cur.execute("SELECT closingPrice FROM %s" % (name,))
    y_data = cur.fetchall()
    y1 = []
    for i in y_data:
        y1.append(i[0])
    print("here")
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
                plot_bgcolor= colors['background'],
                paper_bgcolor= colors['background'], 
                font= {
                    'color': colors['text']
                },
                xaxis=dict(
                    gridcolor= '#459894'
                ),
                yaxis=dict(
                    gridcolor= '#459894'
                )
            )
        }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True) 
