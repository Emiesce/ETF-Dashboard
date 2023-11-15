import random
import pandas as pd
import dash
from dash import html, Input, Output, ALL
import dash_html_components as html
import dash_ag_grid as dag

dash.register_page(__name__)

# variables
# clients = ['Client1', 'Client2', 'Client3', 'Client4', 'Client5', 'Client6', 'Client7', 'Client8', 'Client9', 'Client10', 'Client11', 'Client12', 'Client13', 'Client14', 'Client15', 'Client16', 'Client17', 'Client18', 'Client19', 'Client20', 'Client21', 'Client22', 'Client23', 'Client24', 'Client25', 'Client26', 'Client27', 'Client28', 'Client29', 'Client30']  # J.P. Morgan institutional clients
# groups = ['Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6']  # Groups
# etfs = ['JEPI', 'JPST', 'BBJP', 'JEPQ', 'BBCA', 'BBEU', 'JIRE', 'BBAX', 'BBIN', 'JMST', 'JQUA', 'BBUS', 'BBAG', 'JCPB', 'BBMC', 'JEMA', 'JGLO', 'JMEE', 'JPLD', 'BBRE', 'JPIE', 'JMUB', 'JVAL', 'BBSC', 'JPMB', 'JAVA', 'JGRO', 'BBEM', 'JCPI', 'JPUS', 'BBHY', 'JPSE', 'JPIB', 'JPIN', 'JPRE', 'JPME', 'JMOM', 'JSCP', 'JPEM', 'JPEF', 'JMSI', 'JMHI', 'JBND', 'JIG', 'HELO', 'BBLB', 'BBCB', 'BLLD', 'BBSA', 'TEMP', 'UPWD', 'JIVE', 'JCHI', 'JPSV', 'CIRC', 'JDOC', 'BBIP', 'JTEK', 'BBIB', 'JCTR', 'BBSB']

# num_clients = random.randint(25, 30)  # Number of clients (random between 25 and 30)
# num_groups = random.randint(5, 6)  # Number of groups (random between 5 and 6)
# clients_per_group = num_clients // num_groups  # Number of clients per group

# random.shuffle(clients)  # Shuffle the client list
# random.shuffle(etfs)  # Shuffle the ETF list

# data = []
# print(f"{num_clients=}")
# print(f"{num_groups=}")
# print(f"{clients_per_group=}")
# for i in range(num_clients):
#     if i > clients_per_group * num_groups - 1:
#         print(f"Break at: {i}")
#         break
#     client = clients[i]
#     # print(f"{i=}")
#     group = groups[i // clients_per_group]
#     selected_etfs = random.sample(etfs, random.randint(5, 10))
#     row = {'Client': client, 'Group': group}
#     for j, etf in enumerate(selected_etfs):
#         row[f'ETF{j+1}'] = etf
#     data.append(row)
#     # print(data)

# df = pd.DataFrame(data)

clients = [
    'ABP (Stichting Pensioenfonds ABP)', 
    'GIC Private Limited', 
    'Bank of Japan', 
    'National Pension Service', 
    'Government Pension Investment Fund (Japan)', 
    'China Investment Corporation', 
    'Temasek Holdings', 
    'Korea Investment Corporation', 
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

# Create the Dash app
layout = html.Div([
    
    html.Div([
        
        html.Div([
            html.Img(src="../assets/Icons/IconInstitution.svg", className="w-[25px] h-[25px]"),
            html.Span("Institutional Clients", className="text-[18px] font-medium"),
        ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze bg-white"),
        
        # dcc.Input(id='search-input', type='text', placeholder='Search Clients...', className="py-[6px] px-[10px] mb-[10px] border border-[#AAAAAA] rounded-md"),
        # html.Div(
        #     [
        #         html.H2('JP Morgan Institutional Clients', style={'color': '#004589'}),
        #         dcc.Input(id='search-input', type='text', placeholder='Search clients...', style={'margin-bottom': '10px'})
        #     ], className='header'
        # ),

        
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
                
                # html.Div(
                #     [
                #         html.H3('Clients', style={'color': '#004589'}),
                #         html.Div(id='client-list', style={'overflow': 'scroll', 'height': 'calc(100vh - 140px)'})
                #     ], className='sidebar'
                # ),

                html.Div(id='client-details', className='client-details'),
                html.Div(id='recommendations-container', className='recommendations-container')
            ]
        ),
        
    ], className="flex flex-col gap-2 w-[400px]"),

    html.Div([
            
        html.Div([
            
            html.Div([
            
                html.Img(src="../assets/Icons/IconClient.png", className="w-[75px] h-[75px] rounded-full"),
                
                html.Div([
                    html.Span("Client Name", className="text-[18px] font-medium"),
                    html.Span("Description")
                ], className="flex flex-col gap-2 pb-2"),
            
            ], className="p-4 flex items-center min-w-[40%] gap-4 bg-white drop-shadow-lg rounded-lg"),
            
            html.Div([
                html.Span("ETF Holdings", className="text-[18px] font-medium")
            ], className="p-4 flex flex-col w-full bg-white drop-shadow-lg rounded-lg")
            
        ], className="flex gap-4 min-h-[25%]"),
        
        html.Div([
            
            html.Div([
                "Placeholder"
            ], className="p-4 flex min-w-[21.7%] bg-white drop-shadow-lg rounded-lg"),
            
            html.Div([
                
                html.Div(
                    [
                        html.H3('ETF 1', style={'color': 'white'}),
                        html.P('ETF name: JEPI'),
                        html.P('Flows: 124,058'),
                        html.P('AUM: $29.56 billion'),
                        html.P('Sharpe Ratio: 0.5'),
                    ],
                    className='p-4 w-[200px] h-[170px] text-white bg-navy rounded-[20px]',
                ),
                    
                html.Div(
                    [
                        html.H3('ETF 2', style={'color': 'white'}),
                        html.P('ETF name: JMOM'),
                        html.P('Flows: 123,456'),
                        html.P('AUM: $10.23 billion'),
                        html.P('Sharpe Ratio: 0.7'),
                    ],
                    className='p-4 w-[200px] h-[170px] text-white bg-navy rounded-[20px]',
                ),

                html.Div(
                    [
                        html.H3('ETF3', style={'color': 'white'}),
                        html.P('ETF name: JPIB'),
                        html.P('Flows: 789,012'),
                        html.P('AUM: $50.67 billion'),
                        html.P('Sharpe Ratio: 0.9'),
                    ],
                    className='p-4 w-[200px] h-[170px] text-white bg-jade rounded-[20px]',
                ),
                
                html.Div(
                    [
                        html.H3('ETF 4', style={'color': 'white'}),
                        html.P('ETF name: JMEE'),
                        html.P('Flows: 345,678'),
                        html.P('AUM: $15.89 billion'),
                        html.P('Sharpe Ratio: 0.6'),
                    ],
                    className='p-4 w-[200px] h-[170px] text-white bg-jade rounded-[20px]',
                ),
                
            ], className='flex flex-wrap gap-4'),
            
        ], className="flex gap-4 h-full")
        
    ], className="flex flex-col gap-6 w-full"),
    
], className="p-8 flex gap-8")

# Define callbacks
@dash.callback(
    Output('client-list', 'children'),
    [Input('search-input', 'value')]
)
def display_client_list(search_term):
    if search_term is None:
        filtered_clients = df
    else:
        filtered_clients = df[df['Client'].str.contains(search_term, case=False, na=False)]

    client_elements = [
        html.Div(
            client,
            className='client-item',
            id={'type': 'client-item', 'index': i}
        ) for i, client in filtered_clients['Client'].items()
    ]
    return client_elements or []

@dash.callback(
    Output('client-details', 'children'),
    Input("selection-checkbox-grid", "selectedRows")
)
def display_client_details(selected_rows):
    if not selected_rows:
        return html.Div()
    
    # if client_id is None:
    #     return html.Div()
    
    selected_client = selected_rows[0]["Client"]  # single selection restricted in Ag Grid
    # print(selected_client)
    # print(df)

    client_data = df.loc[df["Client"] == selected_client]
    # print(client_data)
    details = html.Div([
        html.H4('Client Details', style={'color': '#004589'}),
        html.Table([
            html.Tr([html.Th('Group', style={'color': '#575a5d'}), html.Td(client_data['Group'])]),
            html.Tr([html.Th('Client', style={'color': '#575a5d'}), html.Td(client_data['Client'])])
        ])
    ])
    return details

    # client_index = client_id['index']
    # client_data = df.iloc[client_index]
    # details = html.Div([
    #     html.H4('Client Details', style={'color': '#004589'}),
    #     html.Table([
    #         html.Tr([html.Th('Group', style={'color': '#575a5d'}), html.Td(client_data['Group'])]),
    #         html.Tr([html.Th('Client', style={'color': '#575a5d'}), html.Td(client_data['Client'])])
    #     ])
    # ])
    # return details