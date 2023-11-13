import dash
from dash import dcc, html, Input, Output, ALL
import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pages.feature2_backend import find_advantage
from pages.feature2_backend import clean_competitor_data
from pages.feature2_backend import select_column

dash.register_page(__name__)

REGIONS = ["US Equity", "MM Equity", "CN Equity", "BH Equity", "TP Equity"]
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
                
                dcc.Dropdown(
                    id='graph-type',
                    placeholder="Select a Graph Type",
                    options=[
                        {'label': '3D Scatter Plot', 'value': 'scatter_3d'},
                        {'label': '2D Scatter Plot', 'value': 'scatter'},
                        {'label': 'Time_series Plot', 'value': 'time_series'},
                    ],
                ),

                dcc.Dropdown(
                    id='x-variable',
                    placeholder="Select X Variable:",
                    options=[
                        {'label': col, 'value': col} for col in df.columns
                    ],
                ),

                dcc.Dropdown(
                    id='y-variable',
                    placeholder="Select Y Variable:",
                    options=[
                        {'label': col, 'value': col} for col in df.columns
                    ],
                ),

                dcc.Dropdown(
                    id='z-variable',
                    placeholder="Select Z Variable:",
                    options=[
                        {'label': col, 'value': col} for col in df.columns
                    ],
                    #value = 'Avg Dvd Yield'
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
                #select the y variable for time-series plot
                html.Label('Select Variable:', id = 'column-label'),
                dcc.Dropdown(
                    id='column',
                    options=[
                        {'label': col, 'value': col} for col in df1.columns
                    ],
                    value = 'FUND_NET_ASSET_VAL',
                    style={'display': 'none'}
                ),
                
            ], className="flex flex-col gap-4"),
            
            html.Div([
                
                html.Div([
                    html.Img(src="../assets/Icons/IconCompetitor.svg", className="w-[25px] h-[25px]"),
                    html.Span("Competitor ETFs", className="text-[18px] font-medium")
                ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze mb-2"),

                # html.Label('Select Competitor ETFs:'),
                
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
            
            dcc.Graph(id="graph", className="h-[600px] -mt-4 border-b-2 border-bronze"),#, className="py-8 flex justify-center gap-12"),
            
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
        Output("selected-competitors", "children"),
        Output("selected-competitors", "className")
    ],
    Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_selected_rows"),
)
def show_selected_competitors(selected_ticker_indices):
    if None in selected_ticker_indices:
        return "", "hidden"
    
    ticker_values = []
    for region_ind, region_dt in enumerate(selected_ticker_indices):
        for ticker_ind in region_dt:
            region = REGIONS[region_ind]
            ticker = df_v2[region].iloc[ticker_ind]["Ticker"]
            ticker_values.append(ticker)
    
    return [html.Div([
        html.Span(ticker, className="text-jade font-medium text-[14px]")
    ], className="px-4 py-2 bg-gray-light rounded-[20px]") for ticker in ticker_values], "flex flex-wrap gap-2 mb-2 rounded-lg"

#update selector according to graph-type selected
@dash.callback(
    Output('x-variable', 'style'),
    Output('y-variable', 'style'),
    Output('z-variable', 'style'),
    Output('period', 'style'),
    Output('column', 'style'),
    Output('x-label', 'style'),
    Output('y-label', 'style'),
    Output('z-label', 'style'),
    Output('period-label', 'style'),
    Output('column-label', 'style'),
    Input('graph-type', 'value')
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
    Output("graph", "figure"),
    Input("graph-type", "value"),
    Input("x-variable", "value"),
    Input("y-variable", "value"),
    Input("z-variable", "value"),
    Input("period", "value"),
    Input("column", "value"),
    Input({"type": "ticker-selection", "index": ALL }, "derived_virtual_selected_rows"),
    #dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_data"),
    #dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_selected_rows"),
    prevent_initial_call=True
)
def update_graph(
    graph_type, x_variable, y_variable, z_variable, time_period, column, selected_ticker_indices #rows, selected_rows
):
    #print(rows)
    #print(selected_rows)
    #print(selected_ticker_indices)
    
    # selected_Tickers = [
    #     rows[row]["Ticker"] for row in selected_rows
    # ] if selected_rows else "None"

    selected_tickers = []
    for region_ind, region_dt in enumerate(selected_ticker_indices):
        for ticker_ind in region_dt:
            region = REGIONS[region_ind]
            ticker = df_v2[region].iloc[ticker_ind]["Ticker"]
            selected_tickers.append(ticker)
    #print(selected_tickers)
    
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
        if len(selected_tickers) == 2:
            etf1 = selected_tickers[0]
            etf2 = selected_tickers[1]
            period = int(time_period) # Set the desired period length for the time series

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
        return "self-center pt-4 w-fit" #"absolute top-[30%] right-[10px] p-4 border border-gray-medium rounded-lg"

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


