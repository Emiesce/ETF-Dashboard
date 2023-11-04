import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

tailwind_cdn = "https://cdn.tailwindcss.com"
app = Dash(__name__, use_pages = True, external_scripts=[
    tailwind_cdn,
    { "src": "./assets/tailwind_config.js" }
]) # Access Multiple Pages

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div([
    
        html.Div([
        
            html.Div([
                
                html.Div([
                    html.Img(src="./assets/Icons/IconJPM_AM.svg", className="w-[96px] h-[31px]"),
                    
                    html.Img(src="./assets/Icons/IconDDP.svg", className="h-[31px]"),
                ], className="flex gap-2 items-center"),
                
                html.Div([
                    'ETF Dashboard by Team 2 - Minerva'
                ], className="text-center text-[28px]"),
            ], className="flex gap-8 items-center font-medium"),

            html.Div([
                dcc.Link(page['name'], id=page["name"], href=page['path'], className="px-4 py-2 border border-gray-medium rounded-lg focus:bg-aqua focus:text-white hover:bg-aqua hover:text-white", ) for page in dash.page_registry.values()
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
