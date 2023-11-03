import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__, use_pages = True) # Access Multiple Pages

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(
    children=[
        html.Div(children='Minerva ETF Dasshboard', style={'textAlign': 'center', 'fontSize': 50}),

        html.Div([
            dcc.Link(page['name']+" | ", href=page['path']) for page in dash.page_registry.values()
        ]),
        html.HR(),

        # dcc.Graph(
        #     id='example-graph',
        #     figure=fig
        # )
        dash.page_container
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
