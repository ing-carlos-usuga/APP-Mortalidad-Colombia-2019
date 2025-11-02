

# Autor: Carlos Jesús Úsuga Rozo

import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc


# RUTAS Y ARCHIVOS

DATA_DIR = "data"
FILE_MUERTES = os.path.join(DATA_DIR, "Anexo1.NoFetal2019_CE_15-03-23.xlsx")
FILE_DIVIPOLA = os.path.join(DATA_DIR, "Divipola_CE_.xlsx")


# FUNCIONES DE CARGA


def cargar_datos():
    try:
        df = pd.read_excel(FILE_MUERTES)
        print(f"Datos cargados correctamente ({len(df)} registros).")
        return df
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        return pd.DataFrame()

def cargar_divipola():
    try:
        div = pd.read_excel(FILE_DIVIPOLA)
        posibles_cols = [c for c in div.columns if "depart" in c.lower()]
        if len(posibles_cols) >= 2:
            codigo_col, nombre_col = posibles_cols[:2]
            div = div.rename(columns={codigo_col: "COD_DEPARTAMENTO", nombre_col: "NOMBRE_DEPTO"})
            div["COD_DEPARTAMENTO"] = div["COD_DEPARTAMENTO"].astype(str).str.zfill(2)
            return div[["COD_DEPARTAMENTO", "NOMBRE_DEPTO"]]
        return pd.DataFrame()
    except Exception as e:
        print(f"Error al cargar Divipola: {e}")
        return pd.DataFrame()

def cargar_ciudades():
    try:
        div = pd.read_excel(FILE_DIVIPOLA)
        posibles_cols = [c for c in div.columns if "muni" in c.lower()]
        if len(posibles_cols) >= 2:
            codigo_col, nombre_col = posibles_cols[:2]
            div = div.rename(columns={codigo_col: "COD_MUNICIPIO", nombre_col: "NOMBRE_MUNICIPIO"})
            div["COD_MUNICIPIO"] = div["COD_MUNICIPIO"].astype(str).str.zfill(5)
            print("Códigos y nombres de municipios cargados correctamente.")
            return div[["COD_MUNICIPIO", "NOMBRE_MUNICIPIO"]]
        else:
            print("No se detectaron columnas de municipios válidas en Divipola.")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error al cargar municipios: {e}")
        return pd.DataFrame()


# VISUALIZACIONES


def grafico_mapa_departamentos(df, div):
    agg = df.groupby("COD_DEPARTAMENTO").size().reset_index(name="total")
    agg["COD_DEPARTAMENTO"] = agg["COD_DEPARTAMENTO"].astype(str).str.zfill(2)
    agg = agg.merge(div, on="COD_DEPARTAMENTO", how="left")

    fig = px.bar(
        agg.sort_values("total", ascending=False),
        x="NOMBRE_DEPTO",
        y="total",
        text="total",
        title="Distribución total de muertes por departamento (2019)",
        labels={"NOMBRE_DEPTO": "Departamento", "total": "Total de muertes"}
    )
    fig.update_traces(marker_color="indigo", textposition="outside")
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def grafico_lineas_mes(df):
    df_mes = df.groupby("MES").size().reset_index(name="total")
    fig = px.line(df_mes, x="MES", y="total", markers=True,
                  title="Total de muertes por mes (2019)",
                  labels={"MES": "Mes", "total": "Número de muertes"})
    return fig

def grafico_top5_ciudades_violentas(df):
    homicidios = df[df["COD_MUERTE"].astype(str).str.contains("X95", na=False)]
    top5 = homicidios.groupby("COD_MUNICIPIO").size().reset_index(name="total").sort_values("total", ascending=False).head(5)
    fig = px.bar(top5, x="COD_MUNICIPIO", y="total", text="total",
                 title="Top 5 ciudades más violentas (homicidios X95)",
                 labels={"COD_MUNICIPIO": "Ciudad", "total": "Casos"})
    fig.update_traces(marker_color="crimson", textposition="outside")
    return fig

def grafico_circular_ciudades_menor_mortalidad(df, ciudades):
    menores = df.groupby("COD_MUNICIPIO").size().reset_index(name="total").sort_values("total", ascending=True).head(10)
    menores["COD_MUNICIPIO"] = menores["COD_MUNICIPIO"].astype(str).str.zfill(5)
    menores = menores.merge(ciudades, on="COD_MUNICIPIO", how="left")

    menores["Etiqueta"] = menores.apply(
        lambda x: f"{x['COD_MUNICIPIO']} – {x['NOMBRE_MUNICIPIO']}" if pd.notnull(x['NOMBRE_MUNICIPIO']) else x['COD_MUNICIPIO'],
        axis=1
    )

    fig = px.pie(
        menores,
        names="Etiqueta",
        values="total",
        title="10 ciudades con menor índice de mortalidad (nombre y código DANE)",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textinfo="percent+label", textposition="inside")
    return fig

def tabla_causas_principales(df):
    causas = df.groupby(["COD_MUERTE", "MANERA_MUERTE"]).size().reset_index(name="total")
    top10 = causas.sort_values("total", ascending=False).head(10)
    return top10

def grafico_barras_apiladas(df, div):
    agg = df.groupby(["COD_DEPARTAMENTO", "SEXO"]).size().reset_index(name="total")
    agg["COD_DEPARTAMENTO"] = agg["COD_DEPARTAMENTO"].astype(str).str.zfill(2)
    agg = agg.merge(div, on="COD_DEPARTAMENTO", how="left")
    fig = px.bar(agg, x="NOMBRE_DEPTO", y="total", color="SEXO",
                 title="Comparación de muertes por sexo y departamento",
                 labels={"NOMBRE_DEPTO": "Departamento", "total": "Muertes", "SEXO": "Sexo"})
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def histograma_por_grupo_edad(df):
    categorias = {
        "Mortalidad neonatal": range(0, 5),
        "Mortalidad infantil": range(5, 7),
        "Primera infancia": range(7, 9),
        "Niñez": range(9, 11),
        "Adolescencia": [11],
        "Juventud": range(12, 14),
        "Adultez temprana": range(14, 17),
        "Adultez intermedia": range(17, 20),
        "Vejez": range(20, 25),
        "Longevidad / Centenarios": range(25, 29),
        "Edad desconocida": [29]
    }

    def clasificar(grupo):
        for categoria, codigos in categorias.items():
            if int(grupo) in codigos:
                return categoria
        return "Sin información"

    df["CategoriaEdad"] = df["GRUPO_EDAD1"].apply(clasificar)
    fig = px.histogram(df, x="CategoriaEdad",
                       title="Distribución de muertes por grupo de edad (DANE)",
                       color_discrete_sequence=["teal"])
    fig.update_xaxes(title="Categoría de edad (GRUPO_EDAD1)")
    fig.update_yaxes(title="Número de muertes")
    return fig


# DASH APP


app = Dash(__name__)
run = app.run
app.title = "Mortalidad no fetal en Colombia - 2019"

df = cargar_datos()
div = cargar_divipola()
ciudades = cargar_ciudades()
tabla_causas = tabla_causas_principales(df)

app.layout = html.Div([
    # Imagen decorativa superior derecha
    html.Img(
        src="/assets/mortalidad.png",
        style={
            "position": "absolute",
            "top": "20px",
            "right": "40px",
            "width": "250px",
            "height": "auto",
            "border-radius": "10px",
            "box-shadow": "2px 2px 6px rgba(0,0,0,0.3)"
        }
    ),

    html.H1("Carlos Jesús Usuga Rozo", style={"textAlign": "center"}),
    html.H1("Actividad 4: APLICACIONES 1", style={"textAlign": "center"}),
    html.H1("Mortalidad en Colombia - 2019", style={"textAlign": "center"}),
    html.P("Aplicación analítica interactiva con Plotly Dash – Análisis regional y demográfico (Datos DANE 2019).",
           style={"textAlign": "center"}),

    html.Hr(),
    html.H3("Mapa: Distribución de muertes por departamento"),
    dcc.Graph(figure=grafico_mapa_departamentos(df, div)),

    html.H3("Gráfico de líneas: Muertes por mes"),
    dcc.Graph(figure=grafico_lineas_mes(df)),

    html.H3("Top 5 ciudades más violentas (Homicidios X95)"),
    dcc.Graph(figure=grafico_top5_ciudades_violentas(df)),

    html.H3("10 ciudades con menor índice de mortalidad"),
    dcc.Graph(figure=grafico_circular_ciudades_menor_mortalidad(df, ciudades)),

    html.H3("Tabla: 10 principales causas de muerte"),
    html.Table([
        html.Thead(html.Tr([html.Th(col) for col in tabla_causas.columns])),
        html.Tbody([
            html.Tr([
                html.Td(tabla_causas.iloc[i][col]) for col in tabla_causas.columns
            ]) for i in range(len(tabla_causas))
        ])
    ], style={"margin": "auto", "width": "80%", "border": "1px solid black"}),

    html.H3("Muertes por sexo y departamento"),
    dcc.Graph(figure=grafico_barras_apiladas(df, div)),

    html.H3("Histograma: Distribución por grupo de edad"),
    dcc.Graph(figure=histograma_por_grupo_edad(df))
], style={"position": "relative", "padding": "20px"})


# EJECUCIÓN

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)

