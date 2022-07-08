import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

dash.register_page(__name__, path="/nosotros")

style = {"padding": "1rem 1rem"}

layout = html.Div([
    html.H2("Team 181"),
    html.Hr(),
    html.H4("Made with love to help our good friend Bob, who could sell his house and take vacations in the Bahamas.")
], style=style)
