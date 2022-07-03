import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Dash
import base64

# Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL], use_pages=True, suppress_callback_exceptions=True)
server = app.server

# Styles for the content of the page and the navigation bar
navbar_style = {
    "padding": "1rem 1rem",
    "background-color": "#e6cbf5",
}

contenido_style = {"padding": "1rem 1rem"}

# Import the logo of Eukaris
logo = "assets/f1.png"


def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# Basic components of the page
navbar = html.Div([
    dbc.Row([
        dbc.Col([
            html.H4("Eukaris - app para la predicción de precio de inmuebles"),
                dbc.Nav([
                    dbc.NavLink("Inicio", href="/", active="exact"),
                    dbc.NavLink("Resultados", href="/resultados", active="exact"),
                    dbc.NavLink("Team-181", href="/nosotros", active="exact")
                ], pills=True, fill=True)
        ]),
        dbc.Col(html.Img(src=b64_image(logo), style={"width": "35%"}), width={"size":2, "order":"last"})
    ])
], style=navbar_style)

contenido = html.Div(id="contenido-página", children=[], style=contenido_style)

# Page Layout
app.layout = html.Div([
                dcc.Location(id="url"),
                navbar,
                dcc.Store(id="intermediate-value"),
                dcc.Store(id="trial"),
                dash.page_container
                ])

# Run application
if __name__=='__main__':
    app.run_server(debug=False, port=3000)
