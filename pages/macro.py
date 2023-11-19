import pandas as pd
import dash
from dash import html, Input, Output, State, ALL, dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from pages.macro_backend import ticker_list
from pages.macro_backend import macro_list

df1 = pd.read_csv(f'macro data/Interest Rate.csv')
headers = [{'label': col, 'value': col} for col in df1.columns[1:]]

dash.Dash(__name__, suppress_callback_exceptions=True)

dash.register_page(__name__)

dash.Dash(__name__, suppress_callback_exceptions=True)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1('Select an ETF'),
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
                html.H1('Select a Macro Factor'),
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
                        html.H1('Select a Country/Commodity'),
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
                html.H1('Select an Operator'),
                dcc.Dropdown(
                    id='comparison-operator',
                    options=[
                        {'label': 'Greater than', 'value': 'Greater than'},
                        {'label': 'Less than', 'value': 'Less than'},
                        {'label': 'Greater than or Equal to', 'value': 'Greater than or Equal to'},
                        {'label': 'Less than or Equal to', 'value': 'Less than or Equal to'},
                        {'label': 'Increase by', 'value': 'Increase by'},
                        {'label': 'Decrease by', 'value': 'Decrease by'}
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
                html.H1('Enter a Decimal Number:'),
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
        html.Button('Set', 
                    id='set-button', 
                    n_clicks=0, 
                    style={
                        'border': '1px solid #ccc',
                        'padding': '10px',
                        'margin-bottom': '10px'
                    }),
        html.Div(
            id='notification',
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
                'text-align': 'center',
                'width': '100%',
                'height': '100px',
                'margin-bottom': '20px'
            }
            ),
        html.Div(id='selected-values-table', style={'margin': '0 auto', 'width': 'fit-content'})
        # dbc.Modal(
        #     [
        #         dbc.ModalHeader("Notification"),
        #         dbc.ModalBody(dbc.Label("Notification:", id='notification')),
        #         dbc.ModalFooter(
        #             dbc.Button("Close", id="close-button", className="ml-auto", n_clicks=0)
        #         ),
        #     ],
        #     id="modal",
        #     is_open=False,
        # )
        
        
    ],
    style={
        'display': 'flex',
        'flex-wrap': 'wrap'
    }
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
    if n_clicks is not None and n_clicks > clicks and ticker and macro_factor and country and operator and number:
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
        return table
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

clicks2 = 0

#pops up the notification
@dash.callback(
    Output('notification', 'children'),
    # Output('modal', 'is_open'),
    Input('set-button', 'n_clicks'),
    Input('ticker-selector', 'value'),
    Input('macro-factor-selector', 'value'),
    Input('country', 'value'),
    Input('comparison-operator', 'value'),
    Input('number-input', 'value'),
    prevent_initial_call=True
)
def display_selected_values(n_clicks, ticker, macro_factor, country, operator, number):
    global clicks2
    if n_clicks > clicks2 and ticker and macro_factor and country and operator and number:
        clicks2 += 1
        x, line = reminder(macro_factor, country, number, operator)
        if x:
            return html.Div(
                    children=[
                    html.H1('Notification:'),
                    html.H1(f"The {macro_factor} for {country} {line} {number}, time to promote {ticker}")
                    
                ],style={
                'border': '1px solid #ccc',
                'padding': '10px',
                'margin-bottom': '10px',
                'flex': '1',
                'align': 'right'
                }
            )
            # return [f"The {macro_factor} for {country} {line} {number}, time to promote {ticker}", True]
        else:
            return None
            # return None, False
    else:
        return None
        # return None, False
    
    
###TODO make notification a pop up window
# @dash.callback(
#     Output("modal", "is_open", allow_duplicate=True),
#     Output("set-button", "n_clicks"),
#     Input("close-button", "n_clicks"),
#     State("modal", "is_open"),
#     State("set-button", "n_clicks"),
#     prevent_initial_call=True
# )
# def close_modal(n, is_open, n_clicks):
#     if n > 0:
#         return False, 0
#     return is_open, n_clicks