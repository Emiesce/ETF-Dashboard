import random
import pandas as pd
import dash
from dash import html, Input, Output, State, ALL
import dash_core_components as dcc
import dash_mantine_components as dmc
import dash_html_components as html
import dash_ag_grid as dag
import plotly.express as px

dash.register_page(__name__)

clients = [
    'Korea Investment Corporation', 
    'Temasek Holdings', 
    'Canada Pension Plan Investment',
    'NY State Common Retirement Fund',
    'National Pension Service',
    'TX Teachers Retirement System',
    'MI Public School Employees',
    'Florida Retirement System',
    'STRS Ohio',
    'CalSTRS',  # data available up to this client
    'China Investment Corporation', 
    'ABP (Stichting Pensioenfonds ABP)', 
    'GIC Private Limited', 
    'Bank of Japan', 
    'Government Pension Investment Fund (Japan)', 
    'AustralianSuper', 
    'Future Fund (Australia)', 
    'Hong Kong Monetary Authority Investment Portfolio', 
    'Government Pension Fund Global (Norway)', 
    'Employees Provident Fund (Malaysia)', 
    'Khazanah Nasional Berhad', 
    'New Zealand Superannuation Fund', 
    'Ontario Teachers\' Pension Plan', 
    'Reserve Bank of India', 
    'Central Provident Fund (Singapore)', 
    'Public Investment Fund (Saudi Arabia)', 
    'Taiwan Pension Fund Association', 
    'State Administration of Foreign Exchange (China)', 
    'Thailand Government Pension Fund', 
    'Government Investment Corporation of Singapore', 
    'Qatar Investment Authority', 
    'Kuwait Investment Authority', 
    'State Oil Fund of Azerbaijan', 
    'Malaysia Retirement Fund Incorporated', 
    'Korea Teachers Pension Fund', 
    'Central Bank of the Russian Federation', 
    'China Development Bank'
]
clients.sort()

columnDefs = [
    {"field": "Client", "checkboxSelection": True, "headerCheckboxSelection": True},
]

defaultColDef = {
    "flex": 1,
    "width": 350,
    "sortable": True,
    "resizable": True,
    "filter": True,
    "wrapText": True,
    "autoHeight": True,
    "cellStyle": { "wordBreak": "normal", "line-height": "1.25rem" }
}

groups = ['Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6']  # Groups
etfs = ['JEPI', 'JPST', 'BBJP', 'JEPQ', 'BBCA', 'BBEU', 'JIRE', 'BBAX', 'BBIN', 'JMST', 'JQUA', 'BBUS', 'BBAG', 'JCPB', 'BBMC', 'JEMA', 'JGLO', 'JMEE', 'JPLD', 'BBRE', 'JPIE', 'JMUB', 'JVAL', 'BBSC', 'JPMB', 'JAVA', 'JGRO', 'BBEM', 'JCPI', 'JPUS', 'BBHY', 'JPSE', 'JPIB', 'JPIN', 'JPRE', 'JPME', 'JMOM', 'JSCP', 'JPEM', 'JPEF', 'JMSI', 'JMHI', 'JBND', 'JIG', 'HELO', 'BBLB', 'BBCB', 'BLLD', 'BBSA', 'TEMP', 'UPWD', 'JIVE', 'JCHI', 'JPSV', 'CIRC', 'JDOC', 'BBIP', 'JTEK', 'BBIB', 'JCTR', 'BBSB']

num_clients = random.randint(25, 30)  # Number of clients (random between 25 and 30)
num_groups = random.randint(5, 6)  # Number of groups (random between 5 and 6)
clients_per_group = num_clients // num_groups  # Number of clients per group

random.shuffle(etfs)  # Shuffle the ETF list

data = []
for i in range(num_clients):
    if i > clients_per_group * num_groups - 1:
        break
    client = clients[i]
    group = groups[i // clients_per_group]
    selected_etfs = random.sample(etfs, random.randint(5, 10))
    row = {'Client': client, 'Group': group}
    for j, etf in enumerate(selected_etfs):
        etf_details = {
            'Sharpe Ratio': round(random.uniform(0.5, 1.0), 2),
            'Flows': random.randint(1000000, 5000000),
            'AUM': random.randint(50000000, 100000000),
            'Expense Ratio': round(random.uniform(0.02, 0.1), 2)
        }
        row[f'ETF{j+1}'] = etf
        row[f'ETF{j+1} Details'] = etf_details
    data.append(row)

df = pd.DataFrame(data)

RECOMMENDATIONS = ["JEPI US Equity", "JEPQ US Equity", "JIRE US Equity", "BBIN US Equity"]
df_etfs = pd.read_excel("./static/Competitor Data_v2.xlsx", sheet_name="US Equity")
df_recommendations = df_etfs.loc[df_etfs["Ticker"].apply(lambda x: x in RECOMMENDATIONS)].reset_index()

df_client_holdings = pd.read_excel("./static/Client ETF Holdings.xlsx", sheet_name=None)
df_features = pd.read_excel("./static/ETF Recommendations and features.xlsx", sheet_name=None)

# Create the Dash app
layout = html.Div([
    
    html.Div([
        
        html.Div([
            html.Img(src="../assets/Icons/IconInstitution.svg", className="w-[25px] h-[25px]"),
            html.Span("Institutional Clients", className="text-[18px] font-medium"),
        ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze bg-white"),
        
        html.Div(
            [
                html.Span("Select a Client:", className="text-[16px] font-medium"),
                dag.AgGrid(
                    id="selection-checkbox-grid",
                    columnDefs=columnDefs,
                    rowData=list(map(lambda x: { "Client": x }, clients)),
                    defaultColDef=defaultColDef,
                    dashGridOptions={ "rowSelection": "single", "rowHeight": 50, "headerHeight": 0, "pagination": True, "paginationAutoPageSize": True },
                    style={ "height": "500px" }
                ),

                html.Div(id='recommendations-container', className='recommendations-container')
            ]
        ),
        
    ], className="flex flex-col gap-2 w-[400px]"),

    html.Div([
            
        html.Div([
            
            html.Div(id="client-details", children=[
                html.Span("Please Provide a Client", className="text-gray-medium/50 text-center")
            ], className="h-full flex justify-center items-center px-4 py-2 w-[40%] gap-4 bg-white drop-shadow-lg rounded-lg border border-gray-medium border-dashed"),
            
            html.Div(id="etf-holdings-div", children=[
                
                html.Div([
                    
                    html.Span("ETF Holdings", className="border-b-2 border-bronze text-[18px] font-medium"),
                    
                    dmc.Select(
                        id="etf-holding-option",
                        value=5,
                        data=[
                            {"value": 5, "label": "Show Top 5"},
                            {"value": 10, "label": "Show Top 10"},
                        ],
                    ),
                    
                    dmc.Button("See All Holdings", id="modal-holdings-btn", className="w-full bg-aqua mt-auto"),
                    
                    dmc.Modal(
                        title="New Modal",
                        id="modal-holdings",
                        zIndex=10000,
                        children=[
                            html.Div(id="list-etf-holdings"),
                            dmc.Group(
                                [
                                    dmc.Button(
                                        "Close",
                                        color="red",
                                        variant="outline",
                                        id="modal-close-button",
                                    ),
                                ],
                                position="right",
                            ),
                        ]
                    ),
                    
                ], className="flex flex-col gap-2 w-[25%] mr-4"),
                
                
                html.Div(id="list-n-holdings", className="min-w-[35%]"),
                
                dmc.Divider(orientation="vertical", className="mr-[20px]"),
            
                html.Div(id="holdings-graph-div")
            
            ], className="flex-grow gap-4 p-4 flex bg-white drop-shadow-lg rounded-lg")
            
        ], className="flex gap-4 min-h-[32%]"),
        
        
        html.Div(id="recommendation-div", children=[
            
            html.Span("Recommended ETFs", className="pr-4 border-b-2 border-bronze self-start text-[18px] font-medium"),
            
            html.Div(children=[
                            
                html.Div(
                    [
                        html.Span(recommendation["Ticker"], className="text-[16px] font-medium"),
                        html.Span([
                            "AUM: ",
                            html.Span(recommendation["Tot Asset US$ (M)"])
                        ]),
                        html.Span([
                            '1 Year Sharpe Ratio: ',
                            html.Span(recommendation["Sharpe 1Y-M"])
                        ]),
                        html.Span([
                            "1 Year Alpha: ",
                            html.Span(recommendation["Alpha 1Y-M"])
                        ]),
                        html.Div([
                            ">"
                        ], className="mt-auto self-end font-bold bg-white text-navy flex justify-center items-center rounded-full w-[35px] h-[35px]")
                    ],
                    className='flex flex-col p-4 w-[230px] h-[190px] text-white rounded-[20px] bg-navy' if ind % 2 else "flex flex-col p-4 w-[230px] h-[190px] text-white rounded-[20px] bg-jade",
                ) for ind, recommendation in df_recommendations.iterrows()
                
            ], className='flex-grow flex flex-wrap gap-4'),
            
        ], className="flex flex-col items-center gap-2 px-6 py-4 bg-aqua/5 rounded-[20px] drop-shadow-md  w-full")
        
    ], className="flex flex-col gap-4 w-full"),
    
], className="p-8 flex gap-8")

@dash.callback(
    [
        Output('client-details', 'children'),
        Output('client-details', 'className'),
    ],
    Input("selection-checkbox-grid", "selectedRows"),
    prevent_initial_call=True
)
def display_client_details(selected_rows):
    # print(selected_rows)
    if not selected_rows:
        return html.Span("Please Provide a Client", className="text-gray-medium/50 text-center"), "h-full flex justify-center items-center px-4 py-2 w-[40%] gap-4 bg-white drop-shadow-lg rounded-lg border border-gray-medium border-dashed"
    
    selected_client = selected_rows[0]["Client"]  # single selection restricted in Ag Grid
    # print(selected_client)
    # print(df)

    client_data = df.loc[df["Client"] == selected_client]
    client_description_data = df_features["Client Descriptions"]
    client_description = client_description_data.loc[client_description_data["Clients"] == selected_client]
    # print(client_data)
    print(client_description_data.loc[client_description_data["Clients"] == selected_client])
    
    details = html.Div([
    
        html.Img(src="../assets/Icons/IconClient.png", className="w-[75px] h-[75px] rounded-full"),
                
        html.Div([
            
            html.Span(selected_client, className="text-[16px] font-medium"),
            
            dmc.List([
                
                dmc.ListItem([
                    
                    html.Span([
                        "Description: ",
                        html.Span(client_description["Client Descriptions"], className="font-normal whitespace-normal text-ellipsis")
                    ], className="font-medium text-[14px]"),
                    
                
                ]),
                
                dmc.ListItem([
                    
                    html.Span([
                        "Interpretation: ",
                        html.Span(client_description["Interpretations"], className="font-normal whitespace-normal text-ellipsis")
                    ], className="font-medium text-[14px]")
                    
                ])
            ])
        
        ], className="flex flex-col h-full"),
    
    ], className="flex gap-2 items-center")

    return details, "h-full flex justify-center items-center px-4 py-2 w-[40%] gap-4 bg-white drop-shadow-lg rounded-lg"

@dash.callback(
    [
        Output("etf-holdings-div", "className"),
        Output("recommendation-div", "className")
    ],
    Input("selection-checkbox-grid", "selectedRows"),
)
def hide_components(selected_row):
    holding_cn = "hidden"
    recommendation_cn = "hidden"
    if not selected_row:
        return holding_cn, recommendation_cn
    else:
        return "flex-grow gap-4 p-4 flex bg-white drop-shadow-lg rounded-lg", "flex flex-col items-center gap-2 px-6 py-4 bg-aqua/5 rounded-[20px] drop-shadow-md  w-full"

@dash.callback(
    Output("modal-holdings", "opened"),
    Input("modal-holdings-btn", "n_clicks"),
    Input("modal-close-button", "n_clicks"),
    State("modal-holdings", "opened"),
    State("selection-checkbox-grid", "selectedRows"),
    prevent_initial_call=True,
)
def control_modal_holdings(nc1, nc2, opened, selected_row):
    if not selected_row:
        return
    return not opened

@dash.callback(
    [
        Output("modal-holdings", "title"),
        Output("list-etf-holdings", "children"),
    ],
    Input("modal-holdings-btn", "n_clicks"),
    Input("selection-checkbox-grid", "selectedRows"),
)
def populate_modal_holdings(nc, selected_row):
    if not selected_row:
        return "", []
    
    selected_client = selected_row[0]["Client"]
    title = f"All ETF holdings of {selected_client}"
    
    if selected_client not in list(df_client_holdings.keys()):
        return "", []
    
    df_client = df_client_holdings[selected_client]
    # print(df_client)
    content = html.Div([
        
        html.Div([
            html.Span("\u2022 "),
            dmc.Space(w=5),
            html.Span(f"{row['Ticker']}", className="font-medium"),
            html.Span(f"- {row['Full Name']}")
        ], className="flex") for _, row in df_client.iterrows()
    
    ], className="flex flex-col gap-2")

    return title, content

@dash.callback(
    Output("list-n-holdings", "children"),
    Input("etf-holding-option", "value"),
    Input("selection-checkbox-grid", "selectedRows"),
    prevent_initial_call=True
)
def display_n_holdings(num_display, selected_row):
    if not selected_row:
        return "", []
    selected_client = selected_row[0]["Client"]    
    if selected_client not in list(df_client_holdings.keys()):
        return "", []
    
    df_client = df_client_holdings[selected_client][:num_display]
    content = html.Div([
        
        html.Div([
            html.Span("\u2022 "),
            dmc.Space(w=5),
            html.Span(f"{row['Ticker']}"),
        ], className="flex w-fit") for _, row in df_client.iterrows()
    
    ], className="grid grid-rows-5 grid-flow-col gap-[6px]")
    return content

@dash.callback(
    Output("holdings-graph-div", "children"), 
    Input("selection-checkbox-grid", "selectedRows"),
    prevent_initial_call=True
)
def generate_pie_chart(selected_row):
    if not selected_row:
        return "", []
    selected_client = selected_row[0]["Client"]    
    if selected_client not in list(df_client_holdings.keys()):
        return "", []
    
    data = df_client_holdings[selected_client]
    fig = px.pie(data, values="Weight", names="Ticker", hole=0.5)
    fig.update_layout(
        margin={"l":0,"r":0,"t":0,"b":0},
        width=150,
        height=150,
        showlegend=False
    ).update_traces(textinfo="none")
    return dcc.Graph(id="graph", figure=fig)