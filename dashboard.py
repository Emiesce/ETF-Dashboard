import dash
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

tailwind_cdn = "https://cdn.tailwindcss.com"
app = Dash(__name__, use_pages = True, external_scripts=[tailwind_cdn]) # Access Multiple Pages

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div([
    
        html.Div([
        
            html.Div([
                html.Img(src="./assets/IconJPM_AM.svg", className="w-[96px] h-[31px]"),
                
                html.Div([
                    'Minerva ETF Dashboard'
                ], className="text-center text-[24px]"),
            ], className="flex gap-8 items-center font-medium"),

            html.Div([
                dcc.Link(page['name'], href=page['path'], className="px-4 py-2 border rounded-lg hover:bg-[#096183] hover:text-white") for page in dash.page_registry.values()
            ], className="flex justify-center gap-4"),
        ], className="bg-[#f5f7f8] h-[80px] px-4 flex justify-between items-center border-b border-"),
        
        # dcc.Graph(
        #     id='example-graph',
        #     figure=fig
        # )
        
        dash.page_container
    
])

if __name__ == '__main__':
    app.run(debug=True)
