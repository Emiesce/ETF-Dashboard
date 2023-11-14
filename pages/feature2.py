import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pages.feature2_backend import find_advantage
from pages.feature2_backend import clean_competitor_data
from pages.feature2_backend import select_column

dash.register_page(__name__)

# variables
REGIONS = ["US Equity", "MM Equity", "CN Equity", "BH Equity", "TP Equity"]
COLORS = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
]

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

#df = pd.read_csv("./Competitor Data.csv")
df_v2 = pd.read_excel("./static/Competitor Data_v2.xlsx", sheet_name=None)
df = df_v2["Competitor Data"]
df1 = pd.read_csv("price data/JEPI US Equity.csv") #to get columns for time-series plot

layout = html.Div(
    [
        # This Div is responsible for the Selection of Graph Type and Axes
        html.Div([ 

            html.Div([
                
                html.Div([
                    html.Img(src="../assets/Icons/IconGraph.svg", className="w-[25px] h-[25px]"),
                    html.Span("Graph Settings", className="text-[18px] font-medium")
                ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze"),
                
                html.Div([    
                    dcc.Dropdown(
                        id='graph-type',
                        placeholder="Select a Graph Type",
                        options=[
                            {'label': '3D Scatter Plot', 'value': 'scatter_3d'},
                            {'label': '2D Scatter Plot', 'value': 'scatter'},
                            {'label': 'Time_series Plot', 'value': 'time_series'},
                        ],
                    ),
                ]),

                html.Div(id="x-variable-div", children=[
                    dcc.Dropdown(
                        id='x-variable',
                        placeholder="Select X Variable:",
                        options=[
                            {'label': col, 'value': col} for col in df.columns
                        ],
                    ),
                ]),

                html.Div(id="y-variable-div", children=[  
                    dcc.Dropdown(
                        id='y-variable',
                        placeholder="Select Y Variable:",
                        options=[
                            {'label': col, 'value': col} for col in df.columns
                        ],
                    ),
                ]),

                html.Div(id="z-variable-div", children=[
                    dcc.Dropdown(
                        id='z-variable',
                        placeholder="Select Z Variable:",
                        options=[
                            {'label': col, 'value': col} for col in df.columns
                        ],
                        #value = 'Avg Dvd Yield'
                    ),
                ]),
                
                html.Div(id="period-div", children=[
                    dcc.Dropdown(
                        id="period",
                        placeholder="Select Time Period",
                        options=[
                            {"label": "1 month", "value": "30"},
                            {"label": "3 months", "value": "90"},
                            {"label": "6 months", "value": "180"},
                            {"label": "1 year", "value": "365"},
                            {"label": "3 year", "value": "1095"},
                        ],
                        #value = "365",
                    ),
                ]),
                
                #select the y variable for time-series plot
                html.Div(id="column-div", children=[
                    dcc.Dropdown(
                        id='column',
                        placeholder="Select Variable:",
                        options=[
                            {'label': col, 'value': col} for col in df1.columns
                        ],
                        #value = 'FUND_NET_ASSET_VAL',
                    ),
                ])
                
            ], className="flex flex-col gap-4"),
            
            html.Div([
                
                html.Div([
                    html.Img(src="../assets/Icons/IconCompetitor.svg", className="w-[25px] h-[25px]"),
                    html.Span("Competitor ETFs", className="text-[18px] font-medium")
                ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze mb-2"),

                # html.Label('Select Competitor ETFs:'),
                
                # Stores selected competitors
                dcc.Store(id="selected-competitor-data", data={ "tickers": [] }),
                
                # Displays selected competitors
                html.Div([
                    html.Div(id="selected-competitors", children=[
                    ], className=""),
                ], className="flex flex-col gap-2"),
                
                # Displays Competitors in a Selectable List
                dmc.Accordion([
                    dmc.AccordionItem([
                        
                        dmc.AccordionControl(region, className="py-3 text-aqua font-medium focus:bg-gray-light focus:font-bold"),
                        
                        dmc.AccordionPanel([
                                            
                            dash.dash_table.DataTable(
                                id={ "type": "ticker-selection", "index": 0 },
                                columns=[{"name": 'Ticker', "id": 'Ticker'}],
                                data=df_v2[region].to_dict("records"),
                                column_selectable="multi",
                                editable=False,
                                row_selectable="multi",
                                style_table={"overflowY": 20, "font-size": "16px", "width": "100%", "margin-top": "-1rem"},
                                style_cell={"textAlign": "left", "font-family": "system-ui"},
                                style_header={"border": "none", "visibility": "hidden"},
                                style_filter={"background-color": "transparent", "color": "#AAAAAA"},
                                style_data={"border": "none", "background-color": "transparent"},
                                page_size= 10,
                                filter_action="native",
                            ),                    
                                        
                            # dcc.Checklist(
                            #     id={
                            #         "type": "ticker-selection",
                            #         "index": 0
                            #     },
                            #     options=[{"label": html.Span(ticker, className="ml-2"), "value": ticker} for ticker in df_v2[region]["Ticker"]
                            # ], value=[], labelClassName="my-2 ml-2 !flex items-center", inputClassName="min-w-[20px] min-h-[20px] rounded-sm")
                            
                        ], className="bg-aqua/5")
                    ], value=region) for region in REGIONS
                ])            
                
                # dash.dash_table.DataTable(
                #     id="selection-checkbox-grid",
                #     columns=[{"name": 'Ticker', "id": 'Ticker'}],
                #     data=df.to_dict("records"),
                #     column_selectable="multi",
                #     editable=False,
                #     row_selectable="multi",
                #     style_table={"overflowY": 20},
                #     style_cell={"textAlign": "left"},
                #     page_size= 20,
                #     filter_action="native",
                # ),
                # html.Div(id="selection-output"),
            
            ]),
        
        ], className="flex flex-col gap-4"),
        
        html.Div([
            
            html.Div(id="graph-div"),
            #dcc.Graph(id="graph", figure=blank_fig(), className="h-[560px] -mt-4 border-b-2 border-bronze"),#, className="py-8 flex justify-center gap-12"),
            
            html.Div(
                id='advantages-box',
                className="hidden",
                #style={'position': 'absolute', 'top': '30%', 'right': '10px'}
            )
            # dcc.Graph(id='graph', className="p-8 flex justify-center gap-12")
            # html.Div(id='graph-container', style={'display:none'}, className="p-8 flex justify-center gap-12")
        # ],
         
        ], className="w-full flex flex-col")
        
    ], className="p-8 flex gap-8"
)

# Function for showing competitors upon selected
@dash.callback(
    [
        Output("selected-competitor-data", "data"),
        Output("selected-competitors", "children"),
        Output("selected-competitors", "className")
    ],
    [
        Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_indices"),
        Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_selected_rows"),
    ],
    State("selected-competitor-data", "data")
)
def show_selected_competitors(visible_rows, selected_ticker_indices, current_selection: dict[str, list[tuple[int, str]]]):
    # print(f"\n{current_selection=}")
    
    if None in selected_ticker_indices:
        return current_selection, "", "hidden"
    
    ticker_indices = list(map(lambda x: x[0], current_selection["tickers"]))
    ticker_values = list(map(lambda x: x[1], current_selection["tickers"]))
    # print(f"{ticker_indices=}")
    # print(f"{ticker_values=}")
    
    global_ticker_indices = set()
    #print(f"{selected_ticker_indices=}")
    for region_ind, region_dt in enumerate(selected_ticker_indices):
        region = REGIONS[region_ind]
        
        for ticker_ind in region_dt:
            global_ticker_ind = visible_rows[region_ind][ticker_ind]
            global_ticker_indices.add(global_ticker_ind)
            ticker = df_v2[region].iloc[global_ticker_ind]["Ticker"]
            
            # add new selection
            if ticker not in ticker_values:
                current_selection["tickers"].append((global_ticker_ind, ticker))
    #print(f"{global_ticker_indices=}")
    
    # remove deselected options
    deselection = list(set(ticker_indices) - global_ticker_indices)
    #print(f"{deselection=}")
    new_selection = list(filter(lambda x: x[0] not in deselection, current_selection["tickers"]))
    
    #print(f"{new_selection=}\n")
    
    return { "tickers": new_selection }, [html.Div([
        html.Span(ticker, className="text-jade font-medium text-[14px]")
    ], className="px-4 py-2 bg-gray-light rounded-[20px]") for ticker in map(lambda x: x[1], new_selection)], "flex flex-wrap gap-2 mb-2 rounded-lg"

#update selector according to graph-type selected
@dash.callback(
    Output('x-variable-div', 'className'),
    Output('y-variable-div', 'className'),
    Output('z-variable-div', 'className'),
    Output('period-div', 'className'),
    Output('column-div', 'className'),
    Input('graph-type', 'value'),
)
def update_dropdowns(graph_type):
    # Show by default
    x_variable_style = "block"
    y_variable_style = "block"
    z_variable_style = "block"
    period_style = "block"
    column_style = "block"  

    if graph_type == 'scatter_3d':
        period_style = "hidden"
        column_style = "hidden"
        
    elif graph_type == 'scatter':
        z_variable_style = "hidden"
        period_style = "hidden"
        column_style = "hidden"
    
    elif graph_type == 'time_series':
        x_variable_style = "hidden"
        y_variable_style = "hidden"
        z_variable_style = "hidden"
    
    else:
        x_variable_style = "hidden"
        y_variable_style = "hidden"
        z_variable_style = "hidden"
        period_style = "hidden"
        column_style = "hidden" 

    return x_variable_style, y_variable_style, z_variable_style, period_style, column_style

plot_metric = {
    'Tot Asset US$ (M)' : 'FUND_NET_ASSET_VAL',
    'Avg Dvd Yield' : 'TOT_RETURN_INDEX_GROSS_DVDS',
}    

# Function for updating the Graph depending on the selected Graph Type and Axes
@dash.callback(
    Output("graph-div", "children"),
    Input("graph-type", "value"),
    Input("x-variable", "value"),
    Input("y-variable", "value"),
    Input("z-variable", "value"),
    Input("period", "value"),
    Input("column", "value"),
    Input("selected-competitor-data", "data"),
    #Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_selected_rows"),
    #dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_data"),
    #dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_selected_rows"),
    prevent_initial_call=True
)
def update_graph(
    graph_type, x_variable, y_variable, z_variable, time_period, column, selection #rows, selected_rows
):
    #print(rows)
    #print(selected_rows)
    #print(selected_ticker_indices)
    
    # selected_Tickers = [
    #     rows[row]["Ticker"] for row in selected_rows
    # ] if selected_rows else "None"

    selected_tickers = list(map(lambda x: x[1], selection["tickers"]))
    
    figure = {}
    if graph_type == "scatter_3d":
        figure = px.scatter_3d(
            df[df["Ticker"].isin(selected_tickers)],
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
            margin={"l":0,"r":0,"t":0,"b":0},
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.05
            )
        )

    elif graph_type == "scatter":
        figure = px.scatter(
            df[df["Ticker"].isin(selected_tickers)],
            x=x_variable,
            y=y_variable,
            color="Ticker",
        ).update_layout(
            xaxis_title=x_variable,
            yaxis_title=y_variable,
            margin={"t":0,"b":0},
        )
        
    elif graph_type == "time_series":
        if time_period is None or column is None:
            return
        period = int(time_period)
        figure = go.Figure()
        for ind, ticker in enumerate(selected_tickers):
            etf_data = select_column(ticker, column)[:period]
            # print(etf_data)
            etf_data["Date"] = pd.to_datetime(etf_data["Date"])
            etf_trace = go.Scatter(
                x=etf_data["Date"],
                y=etf_data[column],
                name=ticker,
                mode="lines",
                line=dict(color=COLORS[ind])
            )
            figure.add_trace(etf_trace)
        figure.update_layout(
            xaxis_title='Date',
            yaxis_title=column,
            margin={"t":0,"b":0}
        )
        
        # if len(selected_tickers) == 2:
        #     etf1 = selected_tickers[0]
        #     etf2 = selected_tickers[1]
        #     period = int(time_period) # Set the desired period length for the time series

        #     etf1_data = select_column(etf1, column)[:period]
        #     etf2_data = select_column(etf2, column)[:period]
        #     etf1_data['Date'] = pd.to_datetime(etf1_data['Date'])
        #     etf2_data['Date'] = pd.to_datetime(etf2_data['Date'])
            
        #     etf1_trace = go.Scatter(
        #         x=etf1_data['Date'],
        #         y=etf1_data[column],
        #         name=etf1,
        #         mode='lines',
        #         line=dict(color='blue')
        #     )
            
        #     etf2_trace = go.Scatter(
        #         x=etf2_data['Date'],
        #         y=etf2_data[column],
        #         name=etf2,
        #         mode='lines',
        #         line=dict(color='red')
        #     )

        #     figure = go.Figure(data=[etf1_trace, etf2_trace])
        #     figure.update_layout(
        #         xaxis_title='Date',
        #         yaxis_title=column,
        #         margin={"t":0,"b":0}
        #     )
    
    # print(figure)
    return dcc.Graph(id="graph", figure=figure, className="h-[560px] -mt-4 border-b-2 border-bronze")#, className="py-8 flex justify-center gap-12"),


@dash.callback(
    Output("advantages-box", "className"),
    Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_selected_rows")
)
def hide_advantages_box(selected_ticker_indices):
    if None in selected_ticker_indices:
        return "hidden"

    selected = [competitor for region in selected_ticker_indices for competitor in region]
    if len(selected) < 2:
        return "hidden"
    else:
        return "self-center pt-2 w-fit" #"absolute top-[30%] right-[10px] p-4 border border-gray-medium rounded-lg"

# Function for updating the advantages box
@dash.callback(
    Output('advantages-box', 'children'),
    # dash.dependencies.Input('checkbox', 'value'),
    #dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_selected_rows"),
    Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_selected_rows")
)
def update_advantages_box(selected_ticker_indices):
    if None in selected_ticker_indices:
        return

    ticker_values = []
    for region_ind, region_dt in enumerate(selected_ticker_indices):
        for ticker_ind in region_dt:
            region = REGIONS[region_ind]
            ticker = df_v2[region].iloc[ticker_ind]["Ticker"]
            ticker_values.append(ticker)
    #ticker_values = df.loc[selected_options, "Ticker"].tolist()

    if len(ticker_values) < 2:
        return
    
    data_frame = clean_competitor_data(df)

    advantages = find_advantage(data_frame, ticker_values[0], ticker_values[1])
    
    if not advantages.empty:
        advantage_list = []
        max_value = max(advantages.tolist())
        advantage_list.append(html.H2("Fund Comparison: " + ticker_values[0] + " v.s. " + ticker_values[1], className="text-[24px] font-medium mb-2"))
        for index, value in advantages.items():
            if value == max_value and value != float('inf'):
                container = html.Div([
                    html.P(f'{index}:'),
                    html.P(f'{value}% better', className="text-jade font-medium")
                ], className="flex justify-between text-jade font-medium")
            else:
                if value == float('inf') or value == -float('inf'):
                    container = html.Div([
                        html.P(f'{index}:'),
                        html.P('data missing')
                    ], className="flex justify-between")
                else:
                    container = html.Div([
                        html.P(f'{index}:'),
                        html.P(f'{value}% better')
                    ], className="flex justify-between")
            advantage_list.append(container)
    return advantage_list


