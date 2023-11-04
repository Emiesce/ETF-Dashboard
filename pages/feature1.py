import dash
from dash import dcc, html, callback, Output, Input
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
                            
                            dcc.Checklist(id=category, options=[
                                {"label": html.Span(sub_category, className="ml-2"), "value": sub_category} for sub_category in categories[category]
                            ], labelClassName="my-2 ml-2 !flex items-center", inputClassName="min-w-[20px] min-h-[20px] rounded-sm")
                            
                        , className="bg-aqua/5")
                    ], value=category) for category in list(categories.keys())
                ])               
            ])
            
        ], className="flex flex-col gap-2")
        
    ], className="p-4 flex flex-col gap-4 w-[20%] border border-gray-medium rounded-lg"),
    
    html.Div([
        
        html.Div([

            html.Span("You have selected:", className="text-[18px] font-medium"),
            
            html.Div(id="selected_categories", className="flex flex-col gap-2")

        ], className="flex-grow p-4 bg-gray-light rounded-lg"),
        
        html.Hr(className="border-b-2 border-bronze"),
        
        html.Div([], className="min-h-[90%] border border-gray-medium rounded-lg p-4")
    
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
        html.Span(f"{key} > {', '.join(val)}")
    ]) for key, val in selected_categories.items()]