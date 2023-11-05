import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
#from feature2_backend import find_advantage

dash.register_page(__name__)

df = pd.read_csv("example.csv")

layout = html.Div(
    [
        # This Div is responsible for the Selection of Graph Type and Axes
        html.Div([ 
            html.H1('Select a Graph Type:'),

            html.Label('Select Competitor ETFs:'),
            dcc.Checklist(
                id='checkbox',
                options = [
                {'label': 'QQQ', 'value': 'QQQ'},
                {'label': 'SPY', 'value': 'SPY'},
                {'label': 'IVV', 'value': 'IVV'}
                ],
                labelStyle={'display': 'block'}
            ), 
            html.Div(id='selected-div'),

            dcc.Dropdown(
                id='graph-type',
                options=[
                    {'label': '3D Scatter Plot', 'value': 'scatter_3d'},
                    {'label': '2D Scatter Plot', 'value': 'scatter'},
                ],
                value='scatter_3d'
            ),

            html.Label('Select X Variable:'),
            dcc.Dropdown(
                id='x-variable',
                options=[
                    {'label': col, 'value': col} for col in df.columns
                ],
                value = 'Expense Ratio'
            ),

            html.Label('Select Y Variable:'),
            dcc.Dropdown(
                id='y-variable',
                options=[
                    {'label': col, 'value': col} for col in df.columns
                ],
                value = 'ESG Rate'
            ),

            html.Label('Select Z Variable:'),
            dcc.Dropdown(
                id='z-variable',
                options=[
                    {'label': col, 'value': col} for col in df.columns
                ],
                value = 'AUM'
            ),

        ], className="p-4 flex flex-col gap-4 w-[20%] border border-gray-medium rounded-lg"),
        dcc.Graph(id='graph', className="p-8 flex justify-center gap-12")
        # html.Div(id='graph-container', style={'display:none'}, className="p-8 flex justify-center gap-12")
    ], 
    className="p-8 flex justify-center gap-12"
)

# Function for updating the Graph depending on the selected Graph Type and Axes
@dash.callback(
    dash.dependencies.Output('graph', 'figure'),
    dash.dependencies.Input('graph-type', 'value'),
    dash.dependencies.Input('x-variable', 'value'),
    dash.dependencies.Input('y-variable', 'value'),
    dash.dependencies.Input('z-variable', 'value'),
)
def update_graph(graph_type, x_variable, y_variable, z_variable):
    if graph_type == 'scatter_3d':
        figure = px.scatter_3d(df, x=x_variable, y=y_variable, z=z_variable,
            color="Symbol").update_layout(
                scene = dict(
                    xaxis_title=x_variable,
                    yaxis_title=y_variable,
                    zaxis_title=z_variable
                ),
                width=800,
                height=800,
            )

    elif graph_type == 'scatter':
        figure = px.scatter(df, x=x_variable, y=y_variable,
            color="Symbol").update_layout(
                xaxis_title=x_variable,
                yaxis_title=y_variable,
                width=800,
                height=800,
            )

    return figure

@dash.callback(
    dash.dependencies.Output('selected-div', 'children'),
    dash.dependencies.Input('checkbox', 'value')
)
def update_selected_div(selected_options):
    if selected_options:
        selected_divs = []
        for option in selected_options:
            selected_divs.append(html.Div(f'Selected Option: {option}', className='selected-opyion'))
        return selected_divs
    else:
        return []