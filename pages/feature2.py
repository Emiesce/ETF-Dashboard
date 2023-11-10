import dash
from dash import dcc, html
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pages.feature2_backend import find_advantage
from pages.feature2_backend import clean_competitor_data
from pages.feature2_backend import select_column

dash.register_page(__name__)

df = pd.read_csv("./Competitor Data.csv")
df1 = pd.read_csv("price data/JEPI US Equity.csv")

layout = html.Div(
    [
        # This Div is responsible for the Selection of Graph Type and Axes
        html.Div([ 

            html.Label('Select Competitor ETFs:'),
            # Displays Competitors in a Selectable List
            dash.dash_table.DataTable(
                id="selection-checkbox-grid",
                columns=[{"name": 'Ticker', "id": 'Ticker'}],
                data=df.to_dict("records"),
                column_selectable="multi",
                editable=False,
                row_selectable="multi",
                style_table={"overflowY": 20},
                style_cell={"textAlign": "left"},
                page_size= 20,
                filter_action="native",
            ),
            html.Div(id="selection-output"),

            html.H1('Select a Graph Type:'),
            dcc.Dropdown(
                id='graph-type',
                options=[
                    {'label': '3D Scatter Plot', 'value': 'scatter_3d'},
                    {'label': '2D Scatter Plot', 'value': 'scatter'},
                    {'label': 'Time_series Plot', 'value': 'time_series'},
                ],
                value='scatter_3d'
            ),

            html.Label('Select X Variable:', id = 'x-label'),
            dcc.Dropdown(
                id='x-variable',
                options=[
                    {'label': col, 'value': col} for col in df.columns
                ],
                value = 'Avg Dvd Yield',
                style={'display': 'none'}
            ),

            html.Label('Select Y Variable:', id = 'y-label'),
            dcc.Dropdown(
                id='y-variable',
                options=[
                    {'label': col, 'value': col} for col in df.columns
                ],
                value = 'Tot Asset US$ (M)',
                style={'display': 'none'}
            ),

            html.Label('Select Z Variable:', id = 'z-label'),
            dcc.Dropdown(
                id='z-variable',
                options=[
                    {'label': col, 'value': col} for col in df.columns
                ],
                value = 'Avg Dvd Yield',
                style={'display': 'none'}
            ),
            
            html.Label('Select time period:', id = 'period-label'),
            dcc.Dropdown(
                id="period",
                options=[
                    {"label": "1 month", "value": "30"},
                    {"label": "3 months", "value": "90"},
                    {"label": "6 months", "value": "180"},
                    {"label": "1 year", "value": "365"},
                    {"label": "3 year", "value": "1095"},
                ],
                value = "365",
                style={'display': 'none'}
            ),
            
            html.Label('Select Variable:', id = 'column-label'),
            dcc.Dropdown(
                id='column',
                options=[
                    {'label': col, 'value': col} for col in df1.columns
                ],
                value = 'FUND_NET_ASSET_VAL',
                style={'display': 'none'}
            ),


        ], className="p-4 flex flex-col gap-4 w-[20%] border border-gray-medium rounded-lg"),
        html.Div(
            [
                dcc.Graph(id='graph', className="p-8 flex justify-center gap-12"),
                html.Div(
                    id='advantages-box',
                    className="p-4 border border-gray-medium rounded-lg",
                    style={'position': 'absolute', 'top': '30%', 'right': '10px'}
                )
            ],
            style={'position': 'relative', 'flex': '1'}
        )
    ], className="p-8 flex justify-center gap-12"
)

@dash.callback(
    dash.dependencies.Output('x-variable', 'style'),
    dash.dependencies.Output('y-variable', 'style'),
    dash.dependencies.Output('z-variable', 'style'),
    dash.dependencies.Output('period', 'style'),
    dash.dependencies.Output('column', 'style'),
    dash.dependencies.Output('x-label', 'style'),
    dash.dependencies.Output('y-label', 'style'),
    dash.dependencies.Output('z-label', 'style'),
    dash.dependencies.Output('period-label', 'style'),
    dash.dependencies.Output('column-label', 'style'),
    dash.dependencies.Input('graph-type', 'value')
)
def update_dropdowns(graph_type):
    # Show by default
    x_variable_style = {'display': 'block'}
    y_variable_style = {'display': 'block'}
    z_variable_style = {'display': 'block'}
    period_style = {'display': 'block'}  
    column_style = {'display': 'block'}  
    x_label_style = {'display': 'block'}
    y_label_style = {'display': 'block'}
    z_label_style = {'display': 'block'}
    period_label_style = {'display': 'block'}  
    column_label_style = {'display': 'block'}  

    if graph_type == 'scatter_3d':
        period_style = {'display': 'none'}
        period_label_style = {'display': 'none'}
        column_style = {'display': 'none'}
        column_label_style = {'display': 'none'}
    elif graph_type == 'scatter':
        z_variable_style = {'display': 'none'}
        z_label_style = {'display': 'none'}
        period_style = {'display': 'none'}
        period_label_style = {'display': 'none'}
        column_style = {'display': 'none'}
        column_label_style = {'display': 'none'}
    elif graph_type == 'time_series':
        x_variable_style = {'display': 'none'}
        x_label_style = {'display': 'none'}
        y_variable_style = {'display': 'none'}
        y_label_style = {'display': 'none'}
        z_variable_style = {'display': 'none'}
        z_label_style = {'display': 'none'}

    return (
        x_variable_style, y_variable_style, z_variable_style, period_style, column_style
        , x_label_style, y_label_style, z_label_style, period_label_style, column_label_style
    )

plot_metric = {
    'Tot Asset US$ (M)' : 'FUND_NET_ASSET_VAL',
    'Avg Dvd Yield' : 'TOT_RETURN_INDEX_GROSS_DVDS',
}

# Function for updating the Graph depending on the selected Graph Type and Axes
@dash.callback(
    dash.dependencies.Output("graph", "figure"),
    dash.dependencies.Input("graph-type", "value"),
    dash.dependencies.Input("x-variable", "value"),
    dash.dependencies.Input("y-variable", "value"),
    dash.dependencies.Input("z-variable", "value"),
    dash.dependencies.Input("period", "value"),
    dash.dependencies.Input("column", "value"),
    dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_data"),
    dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_selected_rows"),
)
def update_graph(
    graph_type, x_variable, y_variable, z_variable, time_period, column, rows, selected_rows
):
    # print(selected_rows)
    selected_Tickers = [
        rows[row]["Ticker"] for row in selected_rows
    ] if selected_rows else "None"

    if graph_type == "scatter_3d":
        figure = px.scatter_3d(
            df[df["Ticker"].isin(selected_Tickers)],
            x=x_variable,
            y=y_variable,
            z=z_variable,
            color="Ticker",
        ).update_layout(
            scene=dict(
                xaxis_title=x_variable,
                yaxis_title=y_variable,
                zaxis_title=z_variable,
            ),
            width=800,
            height=800,
        )

    elif graph_type == "scatter":
        figure = px.scatter(
            df[df["Ticker"].isin(selected_Tickers)],
            x=x_variable,
            y=y_variable,
            color="Ticker",
        ).update_layout(
            xaxis_title=x_variable,
            yaxis_title=y_variable,
            width=800,
            height=800,
        )
        
    elif graph_type == "time_series":
        if len(selected_Tickers) == 2:
            etf1 = selected_Tickers[0]
            etf2 = selected_Tickers[1]
            # column = x_variable  # Assuming x_variable is the selected column for the time series
            # column = plot_metric[column]
            period = int(time_period) # Set the desired period length for the time series
            # print(time_period)

            etf1_data = select_column(etf1, column)[:period]
            etf2_data = select_column(etf2, column)[:period]
            etf1_data['Date'] = pd.to_datetime(etf1_data['Date'])
            etf2_data['Date'] = pd.to_datetime(etf2_data['Date'])
            
            etf1_trace = go.Scatter(
                x=etf1_data['Date'],
                y=etf1_data[column],
                name=etf1,
                mode='lines',
                line=dict(color='blue')
            )
            
            etf2_trace = go.Scatter(
                x=etf2_data['Date'],
                y=etf2_data[column],
                name=etf2,
                mode='lines',
                line=dict(color='red')
            )

            figure = go.Figure(data=[etf1_trace, etf2_trace])
            figure.update_layout(
                xaxis_title='Date',
                yaxis_title=column,
                width=800,
                height=800
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
    
    
# Function for updating the advantages box
@dash.callback(
    dash.dependencies.Output('advantages-box', 'children'),
    # dash.dependencies.Input('checkbox', 'value'),
    dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_selected_rows"),
)
def update_advantages_box(selected_options):
    if selected_options is None:
        return
    if len(selected_options) < 2:
        return
    data_frame = pd.read_csv('Competitor Data.csv')
    data_frame = clean_competitor_data(data_frame)

    ticker_values = df.loc[selected_options, "Ticker"].tolist()

    advantages = find_advantage(data_frame, ticker_values[0], ticker_values[1])
    
    if not advantages.empty:
        advantage_list = []
        container_style = {'display': 'flex', 'justify-content': 'space-between'}
        max_value = max(advantages.tolist())
        advantage_list.append(html.H2(ticker_values[0] + " v.s. " + ticker_values[1], style={'font-size': '24px'}))
        # advantage_list.append(html.H2("JEPI US Equity v.s. CQQQ US Equity", style={'font-size': '24px'}))
        for index, value in advantages.items():
            # advantage_list.append(html.P(f'{index}:'))
            # advantage_list.append(html.P(f'{value}% better', style={'text-align': 'right'}))
            if value == max_value and value != float('inf'):
                container = html.Div(style=container_style, children=[
                html.P(f'{index}:', style={'color' : 'green'}),
                html.P(f'{value}% better', style={'text-align': 'right', 'color' : 'green'})
            ])
            else:
                if value == float('inf') or value == -float('inf'):
                    container = html.Div(style=container_style, children=[
                    html.P(f'{index}:'),
                    html.P('data missing', style={'text-align': 'right'})
                ])
                else:
                    container = html.Div(style=container_style, children=[
                        html.P(f'{index}:'),
                        html.P(f'{value}% better', style={'text-align': 'right'})
                    ])
            advantage_list.append(container)
    return advantage_list


