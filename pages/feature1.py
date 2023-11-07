import dash
import dash_ag_grid as dag
import plotly.express as px
from dash import dcc, html, callback, Output, Input, State, dash_table
import dash_mantine_components as dmc
from plotly import graph_objects as go
import pandas as pd
import json
import numpy as np

dash.register_page(__name__, path='/')

# dummy variables
SECTORS=["Consumer Discretionary", "Technology", "Financials", "Industrials", "Health care", "Utilities", "Materials", "Real Estate", "Energy", "Communications"]

# data retrieval
categories = None
with open("./static/ETF_categories.json") as file:
    categories = json.load(file)

df_etf = pd.read_excel("./static/JPMorgan_5-ETF-extract.xlsx", usecols=["Name", "Ticker", "Expense Ratio", "Tot Asset US$ (M)", "Tot Ret 1Y", "Top 5 Sector", "Top 5 %NAV"])
df_etf["Top 5 Sector"] = df_etf["Top 5 Sector"].apply(lambda x: x.split(","))
df_etf["Top 5 %NAV"] = df_etf["Top 5 %NAV"].apply(lambda x: x.split(","))
# df_holding = pd.read_excel("./static/JPMorgan_5-ETF-holdings.xlsx", sheet_name=None)  # read all sheets, i.e holdings of all ETFs

df_etf["graph"] = ""
for i, row in df_etf.iterrows():
    df_fig = pd.DataFrame({ "Sector": row["Top 5 Sector"], "%NAV": row["Top 5 %NAV"] })
    
    fig = px.bar(
        df_fig,
        x="Sector",
        y="%NAV",
    )
    
    fig.update_layout(
        showlegend=False,
        yaxis_visible=False,
        yaxis_showticklabels=False,
        xaxis_visible=False,
        xaxis_showticklabels=False,
        margin=dict(l=0, r=0, t=0, b=0),
        template="none",
        yaxis={"categoryorder": "total descending"},
        yaxis_range=[0, 100]
    )
    df_etf.at[i, "graph"] = fig

columnDefs = [
    {
        "field": "Ticker",
        "cellClass": "text-jade font-medium",
    },
    {
        "field": "Name",
        "cellClass": "text-aqua font-medium"
    },
    {
        "field": "graph",
        "cellRenderer": "DCC_GraphClickData",
        "headerName": "Holdings by Sector (%NAV)",
        "maxWidth": 300,
        "minWidth": 100,
    },
    {
        "field": "Expense Ratio",
        "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'},
    },
    {
        "field": "Tot Asset US$ (M)",
        "headerName": "AUM (USD million)"
    },
    {
        "field": "Tot Ret 1Y",
        "headerName": "1 Year Return (%)",
        "valueFormatter": {"function": 'd3.format("(,.2f")(params.value)'}
    }
]

# print(df_etf)
# print(df_holding)

# layout
layout = html.Div([
    
    html.Div([
        
        html.Div([
            html.Img(src="../assets/Icons/IconFilter.svg", className="w-[25px] h-[25px]"),
            html.Span("Filter by Sector(s)", className="text-[18px] font-medium"),
        ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze"),
        
        html.Div([
            
            html.Div([
                
                dmc.Accordion([
                    dmc.AccordionItem([
                        
                        dmc.AccordionControl(category, className="py-3 text-aqua font-medium focus:bg-gray-light focus:font-bold"),
                        
                        dmc.AccordionPanel([
                            
                            html.Button("Select all", id=f"select-all-{category}", n_clicks=None, className="text-bronze hover:underline hover:font-medium hover:cursor-pointer"),
                                
                            dcc.Checklist(id=category, options=[
                                {"label": html.Span(sub_category, className="ml-2"), "value": sub_category} for sub_category in categories[category]
                            ], value=[], labelClassName="my-2 ml-2 !flex items-center", inputClassName="min-w-[20px] min-h-[20px] rounded-sm")
                            
                        ], className="bg-aqua/5")
                    ], value=category) for category in list(categories.keys())
                ])               
            ])
            
        ], className="flex flex-col gap-2")
        
    ], className="p-4 flex flex-col gap-4 w-[20%] border-y border-gray-medium"),
    
    html.Div([
        
        dcc.Store(id="show-selection"),
        
        html.Div([

            html.Span("You have selected:", className="text-[18px] font-medium"),
            
            html.Div(id="selected_categories", className="flex flex-col gap-2 mb-2"),

        ], id="selection-display", className="flex-grow p-4 bg-aqua/5 rounded-lg"),
        
        html.Hr(id="selection-display-hr", className="border-b border-bronze"),
                
        html.Div([
            
            dag.AgGrid(
                rowData=df_etf.to_dict("records"),
                columnSize="sizeToFit",
                columnDefs=columnDefs,
                defaultColDef={"sortable": True, "filter": True, "minWidth": 125},
                dashGridOptions={"rowHeight": 80, "domLayout": "autoHeight"},
                style={"height": None}
            ),
        
        ], className="min-h-[90%]")
        
    ], className="flex flex-grow flex-col gap-4")

], className="p-8 flex justify-center gap-12")    

@callback(Output("selected_categories", "children"),
          [Input(category, "value") for category in list(categories.keys())])
def get_selected_categories(*args):
    selected_categories = {}
    for ind, checklist in enumerate(args):
        if checklist is not None and len(checklist):
            parent = list(categories.keys())[ind]
            selected_categories[parent] = checklist
    #print(selected_categories)
    
    return [html.Div([
        
        html.Span([
            
            f"\u27a4 {key} > ",
            
            html.Span(f"{', '.join(val)}", className="font-normal")
        
        ], className="font-medium")
    ]) for key, val in selected_categories.items()]

@callback(
    [
        Output("selection-display", "className"),
        Output("selection-display-hr", "className")
    ],
    [
        Input(category, "value") for category in list(categories.keys())
    ],
    [
        State("selection-display", "className"),
        State("selection-display-hr", "className")
    ])
def hide_selection(*args):
    # print(args)
    state1, state2 = 'flex-grow p-4 bg-aqua/5 rounded-lg', 'border-b-2 border-bronze'
    selection = list(filter(lambda x: x, args[:-2]))
    return (state1, state2) if len(selection) else ("hidden", "hidden")

# @callback([
#     Output(),
#     Input()
# ])
# def show_selection():
#     pass

# @callback([
#     Output(category, "value") for category in list(categories.keys())
# ], [
#     [Input(f"select-all-{category}", "n_clicks") for category in list(categories.keys())]
# ], [
#     [State(category, "options") for category in list(categories.keys())]
# ])
# def select_all_categories(n_clicks, all_children_options):
#     all_or_none = []
#     for ind, n_click in enumerate(n_clicks):
#         if n_click is not None and n_click % 2 == 1:
#             current = all_children_options[ind]
#             all_or_none.append([option["value"] for option in current])
#         else:
#             all_or_none.append(None)
#     print(all_or_none)
#     return all_or_none