from dash import html

def TitleWithIcon(icon_path: str=None, title: str=None, className: str=None):
    return html.Div([
        html.Img(src=icon_path, className="w-[25px] h-[25px]"),
        html.Span(title, className="text-[18px] font-medium"),
    ], className=className)
    