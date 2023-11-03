import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/')

layout = html.Div(
    [
        dcc.Markdown('# Empty Page 1')
    ]
)