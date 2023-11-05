import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_ag_grid as dag

dash.register_page(__name__)


df = pd.read_csv("example.csv")

columnDefs = [
    {"field": "Symbol", "checkboxSelection": True},
]

defaultColDef = {
    "flex": 1,
    "minWidth": 150,
    "sortable": True,
    "resizable": True,
    "filter": True,
}

layout = html.Div(
    [
        # Displays Competitors in a Selectable List
        dash.dash_table.DataTable(
            id="selection-checkbox-grid",
            columns=[{"name": 'Symbol', "id": 'Symbol'}],
            data=df.to_dict("records"),
            column_selectable="multi",
            editable=False,
            row_selectable="multi",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),
        html.Div(id="selection-output"),

        # This Div is responsible for the Selection of Graph Type and Axes
        html.Div(
            [
                html.H1("Select a Graph Type:"),
                dcc.Dropdown(
                    id="graph-type",
                    options=[
                        {"label": "3D Scatter Plot", "value": "scatter_3d"},
                        {"label": "2D Scatter Plot", "value": "scatter"},
                    ],
                    value="scatter_3d",
                ),

                html.Label("Select X Variable:"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[{"label": col, "value": col} for col in df.columns],
                    value="Expense Ratio",
                ),

                html.Label("Select Y Variable:"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[{"label": col, "value": col} for col in df.columns],
                    value="ESG Rate",
                ),

                html.Label("Select Z Variable:"),
                dcc.Dropdown(
                    id="z-variable",
                    options=[{"label": col, "value": col} for col in df.columns],
                    value="AUM",
                ),
            ],
            className="p-4 flex flex-col gap-4 w-[20%] border border-gray-medium rounded-lg",
        ),
        dcc.Graph(id="graph", className="p-8 flex justify-center gap-12"),
    ],
    className="p-8 flex justify-center gap-12",
)


@dash.callback(
    dash.dependencies.Output("graph", "figure"),
    dash.dependencies.Input("graph-type", "value"),
    dash.dependencies.Input("x-variable", "value"),
    dash.dependencies.Input("y-variable", "value"),
    dash.dependencies.Input("z-variable", "value"),
    dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_data"),
    dash.dependencies.Input("selection-checkbox-grid", "derived_virtual_selected_rows"),
)
def update_graph(
    graph_type, x_variable, y_variable, z_variable, rows, selected_rows
):
    selected_symbols = [
        rows[row]["Symbol"] for row in selected_rows
    ] if selected_rows else None

    if graph_type == "scatter_3d":
        figure = px.scatter_3d(
            df[df["Symbol"].isin(selected_symbols)],
            x=x_variable,
            y=y_variable,
            z=z_variable,
            color="Symbol",
        ).update_layout(
            scene=dict(
                xaxis_title=x_variable,
                yaxis_title=y_variable,
                zaxis_title=z_variable,
            ),
            width=800,
            height=800,
        )

    elif graph_type == "scatter":
        figure = px.scatter(
            df[df["Symbol"].isin(selected_symbols)],
            x=x_variable,
            y=y_variable,
            color="Symbol",
        ).update_layout(
            xaxis_title=x_variable,
            yaxis_title=y_variable,
            width=800,
            height=800,
        )

    return figure


