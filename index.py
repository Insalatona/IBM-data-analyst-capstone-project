import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import vgames, IBMproject_used_techs, IBMproject_desired_techs, IBMproject_demographics


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        [
            html.H2("IBM Project", className="display-4"),
            html.Hr(),
            html.P(
                "Clik on the links below to view the interactive graphs:", className="lead"
            ),
            dbc.NavLink("Technologies Usage", href="/apps/IBMproject_used_techs", active="exact"),
            dbc.NavLink("Desired Technologies", href="/apps/IBMproject_desired_techs", active="exact"),
            dbc.NavLink("Survey Demographics", href="/apps/IBMproject_demographics", active="exact"),
        ],
        style={
            "color": "#CCCCCC",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "30rem",
            "padding": "2rem 1rem",
            "background-color": "black",
        },
    ),
    html.Div(id='page-content', children=[])
])








@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/apps/IBMproject_used_techs":
        return IBMproject_used_techs.layout
    if pathname == "/apps/IBMproject_desired_techs":
        return IBMproject_desired_techs.layout
    if pathname == "/apps/IBMproject_demographics":
        return IBMproject_demographics.layout
    if pathname == "/":
        return IBMproject_used_techs.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)