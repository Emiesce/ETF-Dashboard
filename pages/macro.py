import pandas as pd
import dash
from dash import html, Input, Output, State, ALL, dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash_html_components as html
from pages.macro_backend import ticker_list
from pages.macro_backend import macro_list

### DO NOT refresh the page while using, which may cause some problems for notification and table to show up

df1 = pd.read_csv(f'macro data/Interest Rate.csv')
headers = [{'label': col, 'value': col} for col in df1.columns[1:]]

dash.Dash(__name__, suppress_callback_exceptions=True)

dash.register_page(__name__)

layout = html.Div(
    children=[
        html.H1('Set a Macro Event Reminder', style={'text-align': 'center', 'font-size': '28px', 'margin-top': '20px', 'color': 'grey', 'font-weight': 'bold'}),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1('Select an ETF', style={'font-size': '20px'}),
                        dcc.Dropdown(
                            id='ticker-selector',
                            options=ticker_list,
                            value=None,
                            placeholder='Select a ticker...'
                        )
                    ],style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px',
                        'flex': '1'
                    }
                ),
                html.Div(
                    children=[
                        html.H1('Select a Macro Factor', style={'font-size': '20px'}),
                        dcc.Dropdown(
                            id='macro-factor-selector',
                            options=macro_list,
                            value=None,
                            placeholder='Select a Macro Factor...'
                        )
                    ],style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px',
                        'flex': '1'
                    }
                ),
                html.Div(
                            children=[
                                html.H1('Select a Country/Commodity', style={'font-size': '20px'}),
                                dcc.Dropdown(
                                    id='country',
                                    options=headers,
                                    placeholder='Select a header...'
                                )
                            ],
                            style={
                                'border': '1px solid #ccc',
                                'padding': '10px',
                                'margin-bottom': '10px',
                                'flex': '1'
                            }
                        ),
                html.Div(
                    children=[
                        html.H1('Select an Operator', style={'font-size': '20px'}),
                        dcc.Dropdown(
                            id='comparison-operator',
                            options=[
                                {'label': 'Greater than', 'value': 'Greater than'},
                                {'label': 'Less than', 'value': 'Less than'},
                                {'label': 'Greater than or Equal to', 'value': 'Greater than or Equal to'},
                                {'label': 'Less than or Equal to', 'value': 'Less than or Equal to'},
                                {'label': 'Increase by', 'value': 'Increase by'},
                                {'label': 'Decrease by', 'value': 'Decrease by'},
                                {'label': 'Remain unchanged', 'value': 'Remain unchanged'}
                            ],
                            value=None,
                            placeholder='Select a comparison operator...'
                        )
                    ],
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px',
                        'flex': '1'
                    }
                ),
                html.Div(
                    children=[
                        html.H1('Enter a Decimal Number:', style={'font-size': '20px'}),
                        dcc.Input(
                            id='number-input',
                            type='number',
                            placeholder='Enter a number...',
                            style={'margin-top': '5px'}
                        )
                    ],
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px',
                        'flex': '1'
                    }
                ),
                dmc.Button("Set", 
                        id='set-button', 
                        className="bg-aqua", 
                        style={"display": "flex", "justify-content": "center", "width": "100%"}
                        ),
                # html.Button('Set', 
                #             id='set-button', 
                #             n_clicks=0, 
                #             style={
                #                 'border': '1px solid #ccc',
                #                 'padding': '10px',
                #                 'margin-bottom': '10px'
                #             }),
                dmc.Modal(
                            title="Notification",
                            id="ticker-modal",
                            zIndex=10000,
                            children=[
                                html.Div(id="notification"),
                                dmc.Group(
                                    [
                                        dmc.Button(
                                            "Close",
                                            color="red",
                                            variant="outline",
                                            id="ticker-modal-close-button",
                                            className="mt-4"
                                        ),
                                    ],
                                    position="right",
                                ),
                            ]
                        ),
                html.Div(id='selected-values-table', style={'margin': '50px auto 20px', 'width': 'fit-content'})
                
                
            ],
            style={
                'display': 'flex',
                'flex-wrap': 'wrap',
                'width': '90%',
                'margin': '0 auto'
            }
        )
    ]
)

#update the options in the coutry selector according to macro factor selected
@dash.callback(
    Output('country', 'options'),
    Input('macro-factor-selector', 'value')
)
def update_country_options(factor):
    if factor:
        df = pd.read_csv(f'macro data/{factor}.csv')
        header_options = [{'label': col, 'value': col} for col in df.columns[1:]]
        return header_options
    return []


#store the reminder information in a table 
selected_values = []
clicks = 0
@dash.callback(
    Output('selected-values-table', 'children'),
    Input('set-button', 'n_clicks'),
    Input('ticker-selector', 'value'),
    Input('macro-factor-selector', 'value'),
    Input('country', 'value'),
    Input('comparison-operator', 'value'),
    Input('number-input', 'value'),
    State('selected-values-table', 'children')
    # dash.dependencies.State('selected-values', 'data')
)
def display_selected_values(n_clicks, ticker, macro_factor, country, operator, number, table_children):
    global clicks
    if n_clicks is not None:
        if n_clicks > clicks and ticker and macro_factor and country and operator and number:
            clicks += 1
            values = {
                'Ticker': ticker,
                'Macro Factor': macro_factor,
                'Country/Commodity': country,
                'Operator': operator,
                'Number': number
                
            }
            selected_values.append(values)
            df = pd.DataFrame(selected_values)
            table_title = html.H2('Previous Reminders', style={'text-align': 'center', 'font-weight': 'bold'})
            table = dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in df.columns],
                data=df.to_dict('records'),
                style_table={'border': '1px solid #ccc', 'margin-top': '10px'},
                style_cell={
                    'textAlign': 'center',
                    'minWidth': '150px',
                    'maxWidth': '500px',
                    'whiteSpace': 'normal'
                },
                style_header={'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    {
                        'if': {'column_id': 'Ticker'},
                        'textAlign': 'center'
                    }
                ]
            )
            return [table_title, table]
    return table_children

#function that checks whether is condition is met
def reminder(macro, column, number, operation):
    df = pd.read_csv(f'macro data/{macro}.csv')
    data = df[column]
    # print(data[0])
    if operation == 'Greater than': #Greater than
        if data[0] > number:
            return True, "is greater than"
        else:
            return False, ""
    if operation == 'Less than':
        if data[0] < number: #Less than
            return True, "is less than"
        else:
            return False, ""
    if operation == 'Greater than or Equal to': #greater than or equal to
        if data[0] >= number:
            return True, "is greater than or equal to"
        else:
            return False, ""
    if operation == 'Less than or Equal to':
        if data[0] <= number:
            return True, "is less than or equal to"
        else:
            return False, ""
    if operation == 'Increase by': #increase by more than
        if (data[0]-data[1])/data[1] > number:
            return True, "has increased by more than"
        else:
            return False, ""
    if operation == 'Decrease by': #decrease by more than
        if (data[1]-data[0])/data[1] > number:
            return True, "has decreased by more than"
        else:
            return False, ""
    if operation == 'Remain unchanged': 
        if data[1] == data[0]:
            return True, "has not changed"
        else:
            return False, ""

clicks2 = 0

#pops up the notification
@dash.callback(
    Output('notification', 'children'),
    Output("ticker-modal", "opened", allow_duplicate=True),
    Input('set-button', 'n_clicks'),
    Input('ticker-selector', 'value'),
    Input('macro-factor-selector', 'value'),
    Input('country', 'value'),
    Input('comparison-operator', 'value'),
    Input('number-input', 'value'),
    prevent_initial_call=True,
    allow_duplicate=True
)
def display_selected_values(n_clicks, ticker, macro_factor, country, operator, number):
    global clicks2
    if n_clicks is not None:
        if n_clicks > clicks2 and ticker and macro_factor and country and operator and number:
            clicks2 += 1
            x, line = reminder(macro_factor, country, number, operator)
            if x:
                ticker_text = html.Span(ticker, style={"color": "green"})
                return [[f"The {macro_factor} for {country} {line} {number}, time to promote ", ticker_text], True]
            else:
                return None, False
    else:
        return None, False
    
@dash.callback(
    Output("ticker-modal", "opened", allow_duplicate=True),
    Input("ticker-modal-close-button", "n_clicks"),  
    State("ticker-modal", "opened"),
    prevent_initial_call=True,
)
def control_ticker_modal(nc, opened):
    if nc>0:
        return 
    return False
