import dash
import dash_ag_grid as dag
import plotly.express as px
from dash import dcc, html, callback, ctx, Output, Input, State, ALL, MATCH
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
import pandas as pd
import json
import time

from pages.filter_search import get_ETF_similarity
from components.TitleWithIcon import TitleWithIcon

dash.register_page(__name__, path='/')

# variables
SECTORS = ["Consumer Discretionary", "Technology", "Financials", "Industrials", "Health care", "Utilities", "Materials", "Real Estate", "Energy", "Communications"]
SUPPORTED_TICKERS = ["JEPI", "JPST", "JIRE", "JEPQ", "JQUA", "BBIN"]

# data retrieval
categories = None
with open("./static/ETF_categories.json") as file:
    categories = json.load(file)
parent_categories = list(categories.keys())

# read JPM ETF data
df_etf = pd.read_excel("./static/JPMorgan_5-ETF-extract.xlsx", usecols=["Name", "Ticker", "Expense Ratio", "Tot Asset US$ (M)", "Tot Ret 1Y", "Top 5 Sector", "Top 5 %NAV"])
df_etf["Top 5 Sector"] = df_etf["Top 5 Sector"].apply(lambda x: x.split(","))
df_etf["Top 5 %NAV"] = df_etf["Top 5 %NAV"].apply(lambda x: x.split(","))
df_etf["Name"] = df_etf[["Name", "Ticker"]].apply(lambda x: ",".join(x), axis=1)

# read holdings of JPM ETFs
df_holding = pd.read_excel("./static/JPMorgan_5-ETF-holdings.xlsx", sheet_name=None)  # read all sheets, i.e holdings of all ETFs

# read %NAV by sector of JPM ETFs
df_nav_perct = pd.read_excel("./static/JPMorgan_5-ETF-composition.xlsx", sheet_name=None)

# generate bar charts of %NAV by sector and store in new column
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

# Ag Grid config
columnDefs = [
    {
        "field": "Name",
        "cellClass": "text-aqua font-medium",
        "cellRenderer": "ShowNameAndTicker",
        "minWidth": 250,
        "maxWidth": 300
    },
    {
        "field": "graph",
        "cellRenderer": "DCC_GraphClickData",
        "headerName": "Holdings by Sector (%NAV)",
        "minWidth": 250,
        "maxWidth": 400,
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
            
            # keyword query
            TitleWithIcon(
                icon_path="../assets/Icons/IconKeyword.svg",
                title="Filter by Keyword",
                className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze"
            ),
            
            html.Div([

                dmc.TextInput(
                    id="keyword-input",
                    placeholder="Enter Keyword",
                    className="w-full"
                ),

                html.Div([
                    
                    dmc.HoverCard(
                        withArrow=True,
                        width=300,
                        shadow="md",
                        children=[
                            dmc.HoverCardTarget(html.Span("Help", className="text-[14px] text-aqua/70 hover:text-aqua hover:underline hover:cursor-pointer")),
                            dmc.HoverCardDropdown(
                                dmc.Text(
                                    "This first analyses the similarity between the company description of each constituent and the keyword. Then shows the ETF with the highest similarity after weighing on a constituent level",
                                    size="sm",
                                ),
                            ),
                        ],
                        className="bg-none hover:bg-none -mt-4"
                    ),   
                    
                    dmc.Button("Search", id="keyword-search-button", className="bg-aqua")
                    
                ], className="w-full flex justify-between items-center"),
                
                dcc.Store(id="constituent-similarity-data"),
                dcc.Loading(
                    id="loading-1",
                    type="circle",
                    children=[
                        html.Div(id="keyword-search-output", className="w-full min-h-[20px]"),
                        dmc.Modal(
                            title="Ticker Modal",
                            id="ticker-modal",
                            zIndex=10000,
                            children=[
                                html.Div(id="constituent-similarity"),
                                dmc.Group(
                                    [
                                        dmc.Button(
                                            "Close",
                                            color="red",
                                            variant="outline",
                                            id="ticker-modal-close-button",
                                        ),
                                    ],
                                    position="right",
                                ),
                            ]
                        ),
                    ],
                    parent_className="w-full self-center flex justify-center items-center mb-2"
                ),
                                
            ], className="flex flex-col items-end gap-2")

        ], className="flex flex-col gap-2 mb-2"),
        
        
        # filter list on the left
        TitleWithIcon(
            icon_path="../assets/Icons/IconFilter.svg",
            title="Filter by Sector(s)",
            className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze"
        ),
        
        html.Div([
            
            html.Div([
                
                dmc.Accordion([
                    
                    # generate an accordion for each parent category
                    dmc.AccordionItem([
                        
                        dmc.AccordionControl(category, className="py-3 text-aqua font-medium focus:bg-gray-light focus:font-bold"),
                        
                        dmc.AccordionPanel([
                            
                            html.Button("Select all", id=f"select-all-{category}", n_clicks=None, className="text-bronze hover:underline hover:font-medium hover:cursor-pointer"),

                            # generate checklist for each sub-category
                            dcc.Checklist(id=category, options=[
                                {"label": html.Span(sub_category, className="ml-2"), "value": sub_category} for sub_category in categories[category]
                            ], value=[], labelClassName="my-2 ml-2 !flex items-center", inputClassName="min-w-[20px] min-h-[20px] rounded-sm")
                            
                        ], className="bg-aqua/5")
                    ], value=category) for category in parent_categories
                
                ])  
                             
            ])
            
        ], className="flex flex-col gap-2")
        
    ], className="py-4 flex flex-col gap-4 w-[20%]"),
    
    html.Div([
        
        # displays what categories the user has selected, hidden by default  
        html.Div([

            html.Span("You have selected:", className="text-[18px] font-medium"),
            
            dcc.Store(id="filter-data", data=None),
            
            html.Div(id="selected-categories", className="flex flex-col gap-2 mb-2", ),

            html.Div([
                
                html.Button(id="submit-filter", children="Search", className="px-4 py-[6px] border border-gray-medium font-medium hover:bg-aqua hover:text-white rounded-md")
        
            ], className="flex justify-end")

        ], id="selection-display", className="flex-grow p-4 bg-aqua/5 rounded-lg"),
        
        html.Hr(id="selection-display-hr", className="border-b border-bronze"),
        
        # displays filtered JPM ETF data
        html.Div([
            
            dag.AgGrid(
                id="etf-ag-grid",
                rowData=df_etf.to_dict("records"),
                columnSize="sizeToFit",
                columnDefs=columnDefs,
                defaultColDef={"sortable": True, "filter": True, "minWidth": 125},
                dashGridOptions={"rowHeight": 90, "domLayout": "autoHeight"},
                style={"height": None, "width": "100%" }
            ),
        
        ], className="min-h-[90%]")
        
    ], className="flex flex-grow flex-col gap-4")

], className="p-8 flex gap-12")    

# displays filter criteria on selected categories
@callback(
    [
        Output("selected-categories", "children"),
        Output("filter-data", "data")
    ],
    [Input(category, "value") for category in parent_categories])
def get_selected_categories(*args):
    selected_categories = {}
    for ind, checklist in enumerate(args):
        if checklist is not None and len(checklist):
            parent = parent_categories[ind]
            selected_categories[parent] = checklist
    
    return [html.Div([
        
        html.Span([
            
            f"\u27a4 {key} > ",
            
            html.Span(f"{', '.join(val)}", className="font-normal")
        
        ], className="font-medium"),
        
        dcc.Dropdown(
            id={
                "type": "filter-operator",
                "index": 0
            },
            options=[
                { "label": "> Greater than", "value": "g"  },
                { "label": ">= Greater than or equal to ", "value": "geq" },
                { "label": "= Equal to", "value": "eq" },
                { "label": "< Less than", "value": "l" },
                { "label": "<= Less than or equal to", "value": "leq" }
            ],
            placeholder="Operator",
        ),
        
        dcc.Input(
            id={
                "type": "filter-threshold",
                "index": 0
            },
            type="number",
            placeholder="% NAV",
            min=0,
            max=100,
            className="w-[17%] px-[10px] min-h-[36px] border border-[#cccccc] rounded-[5px]"
        )
        
    ], className="flex gap-4 items-center") for key, val in selected_categories.items()], selected_categories

# hide filter criteria section if no categories are selected
@callback(
    [
        Output("selection-display", "className"),
        Output("selection-display-hr", "className")
    ],
    [
        Input(category, "value") for category in parent_categories
    ],
    [
        State("selection-display", "className"),
        State("selection-display-hr", "className")
    ]
)
def hide_selection(*args):
    # print(args)
    state1, state2 = 'flex-grow p-4 bg-aqua/5 rounded-lg', 'border-b-2 border-bronze'
    selection = list(filter(lambda x: x, args[:-2]))
    return (state1, state2) if len(selection) else ("hidden", "hidden")

# applies filter criteria to the JPM ETF data (df_etf) and outputs matching ETFs
@callback(
    Output("etf-ag-grid", "rowData"),
    Input("submit-filter", "n_clicks"),
    [
        State("filter-data", "data"),
        State({"type": "filter-operator", "index": ALL}, "value"),
        State({"type": "filter-threshold", "index": ALL}, "value")
    ],
    prevent_initial_call=True
)
def apply_ETF_filter(n_clicks, selected_categories, operator, threshold):
    # print("Filter criteria:")
    # print(f"\t\u27a4 {selected_categories=}")
    # print(f"\t\u27a4 {operator=}")
    # print(f"\t\u27a4 {threshold=}")
    
    filter_ticker = []
    
    for ETF_name, df_nav in df_nav_perct.items():
        # print(ETF_name)
        for ind, sector in enumerate(list(selected_categories.keys())):
            sector_nav = df_nav.loc[df_nav["Sector"].str.match(sector)]["%NAV"]
            if len(sector_nav) == 0:
                continue
            nav = float(df_nav.loc[df_nav["Sector"].str.match(sector)]["%NAV"].item())
            target_nav = float(threshold[ind])
            op = operator[ind]
            
            if op == "geq" and nav >= target_nav:
                filter_ticker.append(ETF_name)
            
            elif op == "g" and nav > target_nav:
                filter_ticker.append(ETF_name)
                
            elif op == "eq" and nav == target_nav:
                filter_ticker.append(ETF_name)
            
            elif op == "l" and nav < target_nav:
                filter_ticker.append(ETF_name)
                
            elif op == "leq" and nav <= target_nav:
                filter_ticker.append(ETF_name)
  
    df_filter = df_etf[df_etf["Ticker"].apply(lambda x: x in filter_ticker)]
    
    return df_filter.to_dict("records")

@callback(
    [
        Output("keyword-search-output", "children"),
        Output("etf-ag-grid", "rowData", allow_duplicate=True),
        Output("constituent-similarity-data", "data")
    ],
    Input("keyword-search-button", "n_clicks"),
    State("keyword-input", "value"),
    prevent_initial_call=True
)
def keyword_search(n_clicks, keyword):
    similarity_scores, constituent_similarity = get_ETF_similarity(SUPPORTED_TICKERS, keyword)
    # print(similarity_scores)
    similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[:3]

    children = dmc.Accordion([
        dmc.AccordionItem([
            
            dmc.AccordionControl("Show Top 3 Matching ETFs", className="text-[14px] text-aqua"),
            dmc.AccordionPanel(
                
                html.Div([
                    html.Div([
                        html.Span("Ticker"),
                        html.Span("Similarity (%)")
                    ], className="flex justify-between text-jade font-medium pb-1 border-b border-bronze")
                ] +
                [
                    html.Div([
                        html.Span(ticker, id={"type": "ticker-modal-button", "index": ticker}, className="text-aqua hover:underline hover:cursor-pointer"),
                        html.Span(f"{score:.2f}")
                    ], className="flex justify-between") for ticker, score in similarity_scores
                ], className="flex flex-col")
                
            )
            
        ], value="keyword-matches")
        
    ])
    
    # filter ETFs by ticker with highest similarity
    tickers = list(map(lambda x: x[0] + " US Equity", similarity_scores))
    df = df_etf[df_etf["Ticker"].apply(lambda x: x in tickers)]
    
    return children, df.to_dict("records"), constituent_similarity

@callback(
    Output("ticker-modal", "opened"),
    [
      Input({"type": "ticker-modal-button", "index": ALL}, "n_clicks"),
      Input("ticker-modal-close-button", "n_clicks")  
    ],
    State("ticker-modal", "opened"),
    prevent_initial_call=True,
)
def control_ticker_modal(nc1, nc2, opened):
    if all(i is None for i in nc1):
        return 
    return not opened

@callback(
    Output("constituent-similarity", "children"),
    Input({"type": "ticker-modal-button", "index": ALL}, "n_clicks"),
    State("constituent-similarity-data", "data"),
    prevent_initial_call=True
)
def populate_ticker_modal(nc1, data):
    selected_ticker = ctx.triggered_id["index"]
    constituent_similarity_df = pd.DataFrame.from_dict(data[selected_ticker])
    print(constituent_similarity_df)
    return html.Div(selected_ticker)