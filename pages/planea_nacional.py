import streamlit as st
import polars as pl
import helper as hl
import plotly.graph_objects as go


COLS_SCORE = [
    "periodo",
    "grado_nombre",
    "campo",
    "tipo",
    "score",
    "ee",
    "escuelas",
    "estudiantes",
]
COLS_SCORE_NOMBRE = [
    "Aplicación",
    "Grado",
    "Campo",
    "Tipo",
    "Puntaje",
    "Error estándar",
    "Escuelas",
    "Estudiantes",
]
COLS_SCORE_ENT = [
    "periodo",
    "grado_nombre",
    "campo",
    "entidad",
    "puntaje",
    "ee",
    "escuelas",
    "estudiantes",
]
COLS_SCORE_NOMBRE_ENT= [
    "Aplicación",
    "Grado",
    "Campo",
    "Entidad",
    "Puntaje",
    "Error estándar",
    "Escuelas",
    "Estudiantes",
]
COLS_LOGRO = [
    "periodo",
    "grado_nombre",
    "campo",
    "tipo",
    "nivel",
    "porcentaje",
    "escuelas",
    "estudiantes",
]
COLS_LOGRO_NOMBRE = [
    "Aplicación",
    "Grado",
    "Campo",
    "Tipo",
    "Nivel",
    "Porcentaje",
    "Escuelas",
    "Estudiantes",
]
COLS_LOGRO_ENT = [
    "periodo",
    "grado_nombre",
    "campo",
    "entidad",
    "nivel",
    "porcentaje",
    "escuelas",
    "estudiantes",
]
COLS_LOGRO_NOMBRE_ENT = [
    "Aplicación",
    "Grado",
    "Campo",
    "Entidad",
    "Nivel",
    "Porcentaje",
    "Escuelas",
    "Estudiantes",
]
MARGENES = dict(t=30, b=40)

ruta = "data/PLANEA_{m}.parquet"
score = pl.read_parquet(ruta.format(m="score_nacional"))
logro = pl.read_parquet(ruta.format(m="logro_nacional"))

nacional_score = score.filter(pl.col("subpoblacion") == "Nacional")
nacional_logro = logro.filter(pl.col("subpoblacion") == "Nacional")

st.set_page_config(
    page_title="INEE - PLANEA 2015-2018 - Resultados Nacionales",
    page_icon="✅",
    layout="wide",
)

st.title("PLANEA 2015-2018 - Resultados nacionales")
st.image("img/planea.png", width=500)

col_select_1, col_select_2 = st.columns(2)
with col_select_1:
    periodos = nacional_score.get_column("periodo").unique()
    periodo = st.selectbox("Año", options=periodos, index=0)
    score_periodo = nacional_score.filter(pl.col("periodo") == periodo)
    logro_periodo = nacional_logro.filter(pl.col("periodo") == periodo)

with col_select_2:
    grados = score_periodo.get_column("grado_nombre").unique()
    grado = st.selectbox("Grado", options=grados, index=0)
    score_grado = score_periodo.filter(pl.col("grado_nombre") == grado)
    logro_grado = logro_periodo.sort(["campo", "tipo"]).filter(
        pl.col("grado_nombre") == grado
    )

campos = score_grado.sort("campo").get_column("campo").unique(maintain_order=True)

for campo in campos:
    st.markdown(f"## {campo}")
    score_campo = score_grado.filter(pl.col("campo") == campo)
    logro_campo = logro_grado.filter(pl.col("campo") == campo)

    col_plot_1, col_plot_2 = st.columns(2, gap="large")
    with col_plot_1:
        score_nacional = score_campo.filter(pl.col("tipo") == "Nacional")["score"][
            0
        ]

        st.markdown("### Puntaje")

        score_plot = go.Figure()
        score_plot.add_hline(
            y=score_nacional,
            name="Media nacional",
            line_color=hl.COLOR_LINEA,
            showlegend=True,
        )
        score_plot.add_trace(
            go.Scatter(
                x=score_campo.sort("tipo").get_column("tipo"),
                y=score_campo.sort("tipo").get_column("score"),
                name="Puntaje",
                text=score_campo.get_column("score").round(2),
                textposition="middle right",
                marker_color=hl.COLOR_PUNTO,
                mode="markers+text",
                error_y=dict(
                    type="data",
                    array=score_campo["ee"],
                    visible=True,
                ),
            )
        )
        score_plot.update_layout(
            margin=MARGENES,
            xaxis_title="Nacional y tipos de escuela",
            yaxis_title="Puntaje",
        )

        score_df = score_campo.select(COLS_SCORE)
        score_df.columns = COLS_SCORE_NOMBRE
        st.plotly_chart(score_plot, key=f"{periodo}{grado}{campo}_score")
        st.dataframe(score_df.to_pandas().set_index("Aplicación"))

    with col_plot_2:
        st.markdown("### Niveles de logro")

        niveles = (
            logro_campo.sort("nivel")
            .get_column("nivel")
            .unique(maintain_order=True)
        )
        plot_logro = go.Figure()
        for nivel in niveles:
            logro_nivel = logro_campo.sort("tipo", descending=True).filter(
                pl.col("nivel") == nivel
            )
            plot_logro.add_trace(
                go.Bar(
                    name=nivel,
                    x=logro_nivel.get_column("porcentaje"),
                    y=logro_nivel.get_column("tipo"),
                    text=logro_nivel["porcentaje"],
                    marker=dict(color=hl.COLOR_BARRA[nivel]),
                    orientation="h",
                )
            )
        plot_logro.update_layout(
            barmode="stack",
            margin=MARGENES,
            xaxis_title="Porcentaje",
            yaxis_title="Nacional y tipos de escuela",
        )

        logro_df = logro_campo.select(COLS_LOGRO)
        logro_df.columns = COLS_LOGRO_NOMBRE
        logro_pivot = logro_df.pivot(
            on="Nivel",
            values="Porcentaje",
            index=["Aplicación", "Grado", "Campo", "Tipo"],
        )
        st.plotly_chart(plot_logro, key=f"{periodo}{grado}{campo}_logro")
        st.dataframe(logro_pivot.to_pandas().set_index("Aplicación"))
