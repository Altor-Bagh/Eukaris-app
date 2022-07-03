import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html, callback
import numpy as np
import plotly.graph_objs as go
from geopy.geocoders import Nominatim

# Link of the page in the directory
dash.register_page(__name__, path="/")

# Variables for the inputs
localidad = ['Santa Fe', 'Usaquén', 'Suba', 'Chapinero', 'Fontibón',
       'Kennedy', 'Engativa', 'Bosa', 'Barrios Unidos', 'San Cristobal',
       'Teusaquillo', 'La Candelaria', 'Puente Aranda',
       'Rafael Uribe Uribe', 'Antonio Nariño', 'Los Mártires',
       'Tunjuelito', 'Usme', 'Ciudad Bolívar']

ubicaciones = {'Santa Fe': 'Zona Centro',
  'Usaquén': 'Zona Norte',
  'Suba': 'Zona Noroccidental',
  'Chapinero': 'Zona Chapinero',
  'Fontibón': 'Zona Occidental',
  'Kennedy': 'Zona Suroccidental',
  'Engativa': 'Zona Occidental',
  'Bosa': 'Zona Suroccidental',
  'Barrios Unidos': 'Zona Chapinero',
  'San Cristobal': 'Zona Sur',
  'Teusaquillo': 'Zona Chapinero',
  'La Candelaria': 'Zona Centro',
  'Puente Aranda': 'Zona Centro',
  'Rafael Uribe Uribe': 'Zona Sur',
  'Antonio Nariño': 'Zona Sur',
  'Los Mártires': 'Zona Centro',
  'Tunjuelito': 'Zona Sur',
  'Usme': 'Zona Sur',
  'Ciudad Bolívar': 'Zona Sur'}

# General style required for correct visualization of the components
style = {"padding": "1rem 1rem"}

# Token to access the map
mapbox_access_token = "pk.eyJ1IjoiYWx0b3ItYmFnaCIsImEiOiJjbDN4a2V6cXkzMTd0M2RwbjhheXM4dW1oIn0.gVUcxM-EHq5Se4_MOv-_4Q"

# Page Layout
layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            html.Div(
                   [
                   dbc.Label("Ingrese la dirección del inmueble"),
                   dbc.Input(id="input-dirección", placeholder='', persistence=True, persistence_type="session",
                             type="text"),
                   dbc.Button("Confirmar dirección", color="danger", n_clicks=0, className="me-1",
                              id="boton_direccion", style={'marginTop' : '10px'})
                   ], style=style
                   ),
            html.Div([
                    dbc.Label("Ingrese la localidad del inmueble"),
                    dcc.Dropdown(options=localidad,
                                 placeholder="",
                                 id="dropdown-localidad",
                                 persistence=True, persistence_type="session"),
                    ],
                    style=style
                    ),
            html.Div([
               dbc.Label("Introduzca el número de habitaciones"),
               dbc.Input(id="input-habitaciones", placeholder="", type="number", min=1,
                         persistence=True, persistence_type="session")
                ],
               style=style
            ),
            html.Div([
               dbc.Label("Introduzca el número de baños"),
               dbc.Input(id="input-baños", placeholder="", type="number", min=1,
                         persistence=True, persistence_type="session")
                ],
               style=style
            ),
            html.Div([
               dbc.Label("Introduzca el área en metros cuadrados"),
               dbc.Input(id="input-m2", placeholder="", type="number", min=10,
                         persistence=True, persistence_type="session")
                ],
               style=style
            ),
            html.Div([
                dbc.Label("¿Qué tipo de inmueble es?"),
                dbc.RadioItems(
                    options=[
                        {'label': 'Casa', 'value': 'Casa'},
                        {'label': 'Apartamento', 'value': 'Apartamento'},
                    ], id='tipo',
                    persistence=True, persistence_type="session"
                )
                ],
                style=style
                )
        ], align="start", width=4),
        dbc.Col([
            html.Div(id="mapa", children=[]),
            html.Hr(),
            html.Div([dbc.Button("Enviar formulario", size="lg", className="me-1",
                                 id="boton_state", n_clicks=0, color="danger")]),
            html.Div(id="alerta", children=[], style=style)
        ], style=style, width=8)
    ])
])


# This function updates what's display in the map, also creates de dataframe with the inputs to pass to the
# prediction function
@callback([Output("mapa", "children"),
           Output("intermediate-value", "data")
           ],
          [Input("boton_direccion", "n_clicks"),
           Input("boton_state", "n_clicks"),
           Input("input-dirección", "value"),
           Input("dropdown-localidad", "value"),
           Input("input-habitaciones", "value"),
           Input("input-baños", "value"),
           Input("input-m2", "value"),
           Input("tipo", "value")
           ])
def crear_mapa_creardf(n_clicks_direccion, n_clicks_formulario, direccion, localidad, habitaciones,
                       baños, area, tipo):

    if n_clicks_direccion == 0:
        lat = 4.654587
        lon = -74.093552
    else:
        locator = Nominatim(user_agent="Altor_geocode")
        location = locator.geocode(direccion + ", Bogotá, Colombia")
        lat = location.latitude
        lon = location.longitude

    data_map = go.Scattermapbox(
        lat=[lon],
        lon=[lat],
        mode='markers'
    )
    layout_mapa = go.Layout(title="Mapa de Bogotá",
                            mapbox=dict(
                                accesstoken=mapbox_access_token,
                                zoom=14,
                                style='open-street-map',
                                bearing=0,
                                center=go.layout.mapbox.Center(
                                    lat=lat,
                                    lon=lon
                                )
                            ))
    figure = go.Figure(data=data_map, layout=layout_mapa)

    if n_clicks_direccion > 0 and n_clicks_formulario > 0:
        zona = ubicaciones[localidad]
        data_pd = pd.DataFrame.from_dict({
            "lat": [lat],
            "lon": [lon],
            "bath_prep": [baños],
            "bedrooms_prep": [habitaciones],
            "area_prep": [area],
            "l4": [zona],
            "l5": [localidad],
            "property_type": [tipo]
        })
        if not data_pd.isnull().values.any():
            data_json = data_pd.to_json(orient="split")
    else:
        data_pd = pd.DataFrame.from_dict({"column": [np.nan]})
        data_json = data_pd.to_json(orient="split")

    return dcc.Graph(figure=figure), data_json


# This function creates warnings to let the user know if there's missing information for the prediction
# or if everything is ok to make the prediction
@callback(
    Output("alerta", "children"),
    [Input("boton_state", "n_clicks"),
     Input("intermediate-value", "data")]
)
def crear_alerta(n_clicks, data):
    df = pd.read_json(data, orient="split")
    check_NaN = df.isnull().values.any()
    if n_clicks > 0:
        if check_NaN:
            children = dbc.Alert("Por favor diligencia todos los campos para ver el resultado", color="primary")
            return children
        else:
            children = dbc.Alert(["Perfecto! Por favor continúa a la página de resultados"],
                                 color="success")
            return children