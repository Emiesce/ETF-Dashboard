import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from itertools import islice

FEATURES = ["ETF Filter", "Competitor Analysis", "Recommendation", "Macro"]

tailwind_cdn = "https://cdn.tailwindcss.com"
app = Dash(__name__,
           suppress_callback_exceptions=True,
           use_pages = True, # Access Multiple Pages
           external_scripts=[tailwind_cdn, { "src": "./assets/tailwind_config.js" }],  # enable TailwindCSS
    )

app.layout = html.Div([
    
        html.Div([
        
            html.Div([
                
                html.Div([
                    #html.Img(src="./assets/Icons/IconJPM_AM.svg", className="w-[96px] h-[31px]"),
                    
                    #html.Img(src="./assets/Icons/IconDDP.svg", className="h-[31px]"),

                    html.Img(src="./assets/Icons/logo.png", className="h-[50px]"),


                ], className="flex gap-2 items-center"),
                
                html.Div([
                    'ETF Dashboard by Team 2 - Minerva'
                ], className="text-center text-[28px]"),
            ], className="flex gap-8 items-center font-medium"),

            html.Div([
                dcc.Link(FEATURES[ind], id=page["name"], href=page['path'], className="px-4 py-2 border border-gray-medium rounded-lg focus:bg-aqua focus:text-white hover:bg-aqua hover:text-white", ) for ind, page in islice(enumerate(dash.page_registry.values()), 3)
            ], className="flex justify-center gap-4"),
        ], className="bg-gray-light h-[80px] px-4 flex justify-between items-center border-b border-gray-medium text-gray-medium"),
                
        # dcc.Graph(
        #     id='example-graph',
        #     figure=fig
        # )
        
        dash.page_container
    
])

if __name__ == '__main__':
    app.run(debug=True)
