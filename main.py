import streamlit as st
import polars as pl
import plotly.graph_objects as go

COLOR_BARRA = {
    "Nivel 1": "#f3722c",
    "Nivel 2": "#f9c74f",
    "Nivel 3": "#90be6d",
    "Nivel 4": "#577590",
}
COLOR_LINEA = "#b8c0ff"
COLOR_PUNTO = "#4D9DE0"
COLS_SCORE = ["periodo", "grado_nombre", "campo", "tipo", "score", "ee", "escuelas", "estudiantes"]
COLS_SCORE_NOMBRE = [
    "Aplicación",
    "Grado",
    "Campo",
    "Tipo",
    "Puntaje",
    "Error estándar",
    "Escuelas",
    "Estudiantes"
]
COLS_LOGRO = ["periodo", "grado_nombre", "campo", "tipo", "nivel", "porcentaje", "escuelas", "estudiantes"]
COLS_LOGRO_NOMBRE = ["Aplicación", "Grado", "Campo", "Tipo", "Nivel", "Porcentaje", "Escuelas", "Estudiantes"]
MARGENES = dict(t=30, b=40)

ruta = "data/PLANEA_{m}_nacional.parquet"
planea_score = pl.read_parquet(ruta.format(m="score"))
planea_logro = pl.read_parquet(ruta.format(m="logro"))

nacional_score = planea_score.filter(pl.col("subpoblacion") == "Nacional")
nacional_logro = planea_logro.filter(pl.col("subpoblacion") == "Nacional")

### Streamlit ###
st.set_page_config(
    page_title="INEE - Resultados de evaluaciones del aprendizaje",
    page_icon="✅",
    layout="wide",
)

st.title("Resultados nacionales")

col_select_1, col_select_2, col_select_3 = st.columns(3)
with col_select_1:
    periodos = nacional_score.get_column("periodo").unique()
    periodo = st.selectbox("Año", options=periodos, index=0)
    score_periodo = nacional_score.filter(pl.col("periodo") == periodo)
    logro_periodo = nacional_logro.filter(pl.col("periodo") == periodo)

with col_select_2:
    grados = score_periodo.get_column("grado_nombre").unique()
    grado = st.selectbox("Grado", options=grados, index=0)
    score_grado = score_periodo.filter(pl.col("grado_nombre") == grado)
    logro_grado = logro_periodo.filter(pl.col("grado_nombre") == grado)

with col_select_3:
    campos = score_grado.get_column("campo").unique()
    campo = st.selectbox("Campo:", options=campos, index=0)

logro_campo = logro_grado.sort("tipo").filter(pl.col("campo") == campo)
score_campo = score_grado.sort("tipo").filter(pl.col("campo") == campo)

st.markdown(f"## {campo}")

col_plot_1, col_plot_2 = st.columns(2, gap="large")
with col_plot_1:
    score_nacional = score_campo.filter(pl.col("tipo") == "Nacional")["score"][0]

    st.markdown("### Puntaje")

    score_plot = go.Figure()
    score_plot.add_hline(
        y=score_nacional,
        name="Media nacional",
        line_color=COLOR_LINEA,
        showlegend=True,
    )
    score_plot.add_trace(
        go.Scatter(
            x=score_campo.sort("tipo").get_column("tipo"),
            y=score_campo.get_column("score"),
            name="Puntaje",
            text=score_campo.get_column("score").round(2),
            textposition="middle right",
            marker_color=COLOR_PUNTO,
            mode="markers+text",
            error_y=dict(
                type="data",
                array=score_campo["ee"],
                visible=True,
            ),
        )
    )
    score_plot.update_layout(margin=MARGENES)

    score_df = score_campo.select(COLS_SCORE)
    score_df.columns = COLS_SCORE_NOMBRE
    st.plotly_chart(score_plot, key=f"{periodo}{grado}{campo}_score")
    st.dataframe(score_df.to_pandas().set_index("Aplicación"))

with col_plot_2:
    st.markdown("### Niveles de logro")

    niveles = logro_campo.sort("nivel").get_column("nivel").unique(maintain_order=True)
    plot_logro = go.Figure()
    for nivel in niveles:
        logro_nivel = logro_campo.sort("tipo", descending=True).filter(pl.col("nivel") == nivel)
        plot_logro.add_trace(
            go.Bar(
                name=nivel,
                x=logro_nivel.get_column("porcentaje"),
                y=logro_nivel.get_column("tipo"),
                text=logro_nivel["porcentaje"],
                marker=dict(color=COLOR_BARRA[nivel]),
                orientation="h",
            )
        )
    plot_logro.update_layout(barmode="stack", margin=MARGENES)

    logro_df = logro_campo.select(COLS_LOGRO)
    logro_df.columns = COLS_LOGRO_NOMBRE
    logro_pivot = logro_df.pivot(
        on="Nivel", values="Porcentaje", index=["Aplicación", "Grado", "Campo", "Tipo"]
    )
    st.plotly_chart(plot_logro, key=f"{periodo}{grado}{campo}_logro")
    st.dataframe(logro_pivot.to_pandas().set_index("Aplicación"))
