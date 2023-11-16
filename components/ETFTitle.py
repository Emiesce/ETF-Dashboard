from dash import html
import dash_mantine_components as dmc

def ETFTitle(ticker: str=None, full_name: str=None, className: str=None):
    if full_name:
        return html.Div([
            html.Span("\u2022 "),
            dmc.Space(w=5),
            html.Span(ticker, className="font-medium"),
            html.Span(f"- {full_name}")
        ], className=className)
    
    return html.Div([
        html.Span("\u2022 "),
        dmc.Space(w=5),
        html.Span(ticker, className="font-medium")
    ], className=className)