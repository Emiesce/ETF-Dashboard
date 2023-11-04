import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import json

dash.register_page(__name__, path='/')

categories = None
with open("./static/ETF_categories.json") as file:
    categories = json.load(file)

layout = html.Div([
    
    html.Div([
        
        html.Div([
            html.Img(src="../assets/Icons/IconFilter.svg", className="w-[25px] h-[25px]"),
            html.Span("Filter by Sector(s)", className="text-[18px] font-medium"),
        ], className="flex gap-2 items-center"),
        
        html.Div([
            
            dcc.Checklist([
                { "label": html.Span(category, className="ml-2"), "value": category }
            ], labelClassName="!flex items-center", inputClassName="w-[20px] h-[20px] rounded-sm") for category in list(categories.keys())
        
        ], className="flex flex-col gap-2")
    
    ], className="p-4 flex flex-col gap-2 w-[20%] border border-gray-medium rounded-lg"),
    
    html.Div(["Output"], className="flex-grow border rounded-lg")

], className="p-8 flex justify-center gap-12")