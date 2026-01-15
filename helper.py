import polars as pl
import plotly.graph_objects as go

COLOR_BARRA = {
    "Nivel 1": "#f3722c",
    "Nivel 2": "#f9c74f",
    "Nivel 3": "#90be6d",
    "Nivel 4": "#577590",
}

COLOR_LINEA = "#815ac0"

COLOR_PUNTO = "#4D9DE0"

MARGENES = dict(t=30, b=40)

def get_cols(metrica: str, grupo: str, titulo: bool = False) -> list:
    """
    Devuelve una lista con nombres de columnas.

    :param metrica: Uno de "score" o "logro".
    :type metrica: str
    :param grupo: Uno de "nacional" o "entidad".
    :type grupo: str
    :param titulo: Si debe devolver los nombres con formato de título.
    :type titulo: bool
    :return: Una lista con nombres de columnas.
    :rtype: list
    """
    if grupo == "nacional":
        col_grupo = "tipo"
    elif grupo == "entidad":
        col_grupo = "entidad"
    if metrica == "score" and titulo:
        cols = [
            "Aplicación",
            "Grado",
            "Campo",
            col_grupo.title(),
            "Puntaje",
            "Error estándar",
            "Escuelas",
            "Estudiantes",
        ]
    elif metrica == "score":
        cols = [
            "periodo",
            "grado_nombre",
            "campo",
            col_grupo,
            "score",
            "ee",
            "escuelas",
            "estudiantes",
        ]
    elif metrica == "logro" and titulo:
        cols = [
            "Aplicación",
            "Grado",
            "Campo",
            col_grupo.title(),
            "Nivel",
            "Porcentaje",
            "Escuelas",
            "Estudiantes",
        ]
    elif metrica == "logro":
        cols = [
            "periodo",
            "grado_nombre",
            "campo",
            col_grupo,
            "nivel",
            "porcentaje",
            "escuelas",
            "estudiantes",
        ]
    return cols

def get_score_plot(score, grupo, ee, score_nacional=None) -> go.Figure:
    if len(grupo) > 16:
        alto = len(grupo) * 30
        titulo_yaxis = "Entidades"
    else:
        alto = len(grupo) * 65
        titulo_yaxis = "Nacional y tipos de escuela"
    score_plot = go.Figure()
    if score_nacional:
        score_plot.add_vline(
            x=score_nacional,
            name="Media nacional",
            line_color=COLOR_LINEA,
            showlegend=True,
        )
    score_plot.add_trace(
        go.Scatter(
            x=score,
            y=grupo,
            name="Puntaje",
            text=score.round(2),
            textposition="top center",
            marker_color=COLOR_PUNTO,
            mode="markers+text",
            orientation="h",
            error_x=dict(
                type="data",
                array=ee,
                visible=True,
            ),
        )
    )
    score_plot.update_layout(
        xaxis_title="Puntaje con intervalo de confianza al 95%",
        yaxis_title=titulo_yaxis,
        margin=MARGENES,
        height=alto,
    )
    return score_plot

def get_logro_plot(df, grupo) -> go.Figure:
    num_elementos = len(df.get_column(grupo).unique()) 
    if num_elementos > 9:
        alto = num_elementos * 30
    else:
        alto = num_elementos * 65
    if grupo == "tipo":
        titulo_yaxis = "Nacional y tipos de escuela"
    elif grupo == "entidad":
        titulo_yaxis = "Entidades"
    
    niveles = (
        df.sort("nivel").get_column("nivel").unique(maintain_order=True)
        )
    
    plot_logro = go.Figure()
    for nivel in niveles:
            logro_nivel = df.filter(pl.col("nivel") == nivel)
            porcentaje = logro_nivel.get_column("porcentaje")
            tipo = logro_nivel.get_column(grupo)

            plot_logro.add_trace(
                go.Bar(
                    name=nivel,
                    x=porcentaje,
                    y=tipo,
                    text=porcentaje,
                    marker=dict(color=COLOR_BARRA[nivel]),
                    orientation="h",
                )
            )
    plot_logro.update_layout(
        barmode="stack",
        xaxis_title="Porcentaje por nivel de logro",
        yaxis_title=titulo_yaxis,
        margin=MARGENES,
        height=alto,
    )
    return plot_logro