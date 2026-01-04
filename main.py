import streamlit as st
import polars as pl
import plotly.graph_objects as go

COLOR_BARRA = {
    "Nivel 1": "#E15554",
    "Nivel 2": "#E1BC29",
    "Nivel 3": "#3BB273",
    "Nivel 4": "#7768AE",
}

ruta = "data/PLANEA_{m}_nacional.parquet"
planea_score = pl.read_parquet(ruta.format(m="score"))
planea_logro = pl.read_parquet(ruta.format(m="logro"))

nacional_score = planea_score.filter(pl.col("subpoblacion") == "Nacional")
nacional_logro = planea_logro.filter(pl.col("subpoblacion") == "Nacional")

### Streamlit ###
st.title("Resultados nacionales")

col1, col2 = st.columns(2)

periodos = nacional_score.get_column("periodo").unique()
with col1:
    periodo = st.selectbox("Año", options=periodos)
score_periodo = nacional_score.filter(pl.col("periodo") == periodo)
logro_periodo = nacional_logro.filter(pl.col("periodo") == periodo)

grados = score_periodo.get_column("grado_nombre").unique()
with col2:
    grado = st.selectbox("Asignatura", options=grados)
score_grado = score_periodo.filter(pl.col("grado_nombre") == grado)
logro_grado = logro_periodo.filter(pl.col("grado_nombre") == grado)

campos = score_grado.get_column("campo").unique()

for campo in campos:
    st.markdown(f"## {campo}")
    score_campo = score_grado.filter(pl.col("campo") == campo)
    logro_campo = logro_grado.filter(pl.col("campo") == campo)
    score_nacional = score_campo.filter(pl.col("tipo") == "Nacional")["score"][0]
    score_df = score_campo.select(
        ["periodo", "grado_nombre", "campo", "tipo", "score", "ee"]
    )
    score_df.columns = [
        "Aplicación",
        "Grado",
        "Campo",
        "Tipo",
        "Puntaje",
        "Error estándar",
    ]
    plot = go.Figure()
    plot.add_hline(
        y=score_nacional,
        name="Media nacional",
        line_color="#7768AE",
        showlegend=True,
    )
    plot.add_trace(
        go.Scatter(
            x=score_campo.get_column("tipo"),
            y=score_campo.get_column("score"),
            name="Puntaje",
            text=score_campo.get_column("score").round(2),
            textposition="middle right",
            mode="markers+text",
            error_y=dict(
                type="data",
                array=score_campo["ee"],
                visible=True,
            ),
        )
    )
    plot.update_layout(margin=dict(t=30))

    logro_df = logro_campo.select(
        ["periodo", "grado_nombre", "campo", "tipo", "nivel", "porcentaje"]
    )
    logro_df.columns = [
        "Aplicación",
        "Grado",
        "Campo",
        "Tipo",
        "Nivel",
        "Porcentaje",
    ]

    plot_logro = go.Figure()
    for nivel in (
        logro_campo.sort("nivel").get_column("nivel").unique(maintain_order=True)
    ):
        logro_nivel = logro_campo.filter(pl.col("nivel") == nivel)
        plot_logro.add_trace(
            go.Bar(
                name=nivel,
                x=logro_nivel["tipo"],
                y=logro_nivel["porcentaje"],
                marker=dict(color=COLOR_BARRA[nivel]),
            )
        )
    plot_logro.update_layout(barmode="stack")
    st.plotly_chart(plot, key=f"{periodo}{grado}{campo}")
    st.dataframe(score_df.to_pandas().set_index("Aplicación"))
    st.plotly_chart(plot_logro, key=f"{periodo}{grado}{campo}_logro")
    st.dataframe(logro_df.to_pandas().set_index("Aplicación"))
