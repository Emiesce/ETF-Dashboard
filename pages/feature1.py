import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_mantine_components as dmc
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
        ], className="flex gap-2 items-center pb-2 border-b-2 border-b-bronze"),
        
        html.Div([
            
            html.Div([
                
                dmc.Accordion([
                    dmc.AccordionItem([
                        
                        dmc.AccordionControl(category, className="py-3 text-aqua font-medium focus:bg-gray-light focus:font-bold"),
                        
                        dmc.AccordionPanel(
                            
                            dcc.Checklist([
                                {"label": html.Span(sub_category, className="ml-2"), "value": sub_category} for sub_category in categories[category]
                            ], labelClassName="my-2 ml-2 !flex items-center", inputClassName="min-w-[20px] min-h-[20px] rounded-sm")
                            
                        , className="bg-aqua/5")
                    ], value=category) for category in list(categories.keys())
                ])               
            ])
            
        ], className="flex flex-col gap-2")
        
    ], className="p-4 flex flex-col gap-4 w-[20%] border border-gray-medium rounded-lg"),
    
    html.Div(["Output"], className="flex-grow border rounded-lg")

], className="p-8 flex justify-center gap-12")