import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, html, callback
import pandas as pd
import sklearn
from joblib import load

# Link of the page in the directory
dash.register_page(__name__, path="/resultados")

# General style required for correct visualization of the components
style = {"padding": "1rem 1rem"}

# Page Layout
layout = html.Div(children=[], id="div_resultados", style=style)


# helper function to create the cards
def tarjeta_resultados(titulo, contenido):
    children = html.Div([
        html.H3(titulo, className="ms-1"),
        html.Hr(className="my-2"),
        html.H3(contenido, className="ms-1")
    ], className="h-100 p-5 bg-light border rounded-3"
    )
    return children


# The cards and table with the results are wrapped in the same function
@callback(
    Output("div_resultados", "children"),
    Input("intermediate-value", "data")
)
def display_resultados(data):
    df = pd.read_json(data, orient="split")

    if df.isnull().values.any():
        children = dbc.Alert([
            html.H3("Ups!", className="alert-heading"),
            html.P("Parece que hay información incompleta sobre el inmueble."),
            html.P("Por favor, completa los campos faltantes y haz click sobre enviar formulario para ver el precio del inmueble."),
            html.Hr()
        ], color="primary")
        return children

    else:
        pipe = load("data/randomforest_model_1.joblib")
        prediction = pipe.predict(df)[0]

        # Create the cards
        t_precio_general = tarjeta_resultados(titulo="El precio del inmueble es: ", contenido=str("$ " + "{:,}".format(int(prediction))))
        precio_metro = prediction / df.iloc[0, 4]
        t_precio_metro = tarjeta_resultados(titulo="El precio por metro cuadrado es de: ", contenido=str("$ " + "{:,}".format(int(precio_metro))))

        # Create the table
        data = {"Derechos notariales": ["Derechos notariales", "$ " + "{:,}".format(round(int(prediction) * 0.004),0), "$ " + "{:,}".format(round(int(prediction) * 0.004), 0)],
                "IVA": ["IVA", "$ " + "{:,}".format(round(int(prediction) * 0.19),0), "$ " + "{:,}".format(round(int(prediction) * 0.19),0)],
                "Retefuente": ["Retefuente", "$ 0", "$ " + "{:,}".format(round(int(prediction) * 0.01),0)],
                "Boleta fiscal/Benficiencia": ["Boleta fiscal/Benficiencia", "$ " + "{:,}".format(round(int(prediction) * 0.01),0), "$ 0"],
                "Registro": ["Registro", "$ " + "{:,}".format(round(int(prediction) * 0.00861),0), "$ 0"],
                "Otros gastos": ["Otros gastos", "$ " + "{:,}".format(100000), "$ " + "{:,}".format(100000)]}
        dff = pd.DataFrame.from_dict(data, orient="index", columns=["Tipo de gasto", "Comprador", "Vendedor"])
        tabla_resultados = dbc.Table.from_dataframe(dff, striped=True, bordered=True, hover=True)

        # Prepare the page content
        children = dbc.Container([
            dbc.Row([
                dbc.Col(id="resultado-precio", children=[t_precio_general], style=style),
                dbc.Col(id="precio-m2", children=[t_precio_metro], style=style),
                html.Hr()
            ]),
            dbc.Row(
                [html.H3("Gastos notariales adicionales"),
                html.P("Teniendo en cuenta el valor calculado para el inmueble, se deben considerar también los siguientes costos asociados"),
                html.Div(id="tabla_valores", children=[tabla_resultados], style=style)]
            )
        ])
        return children
