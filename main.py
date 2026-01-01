import streamlit as st
import polars as pl
import plotly.graph_objects as go

ruta_data = "data/PLANEA_scores_nacional.parquet"
planea = pl.read_parquet(ruta_data)

nacional = planea.filter(pl.col("subpoblacion") == "Nacional").select(
    [
        "subpoblacion",
        "grupo",
        "tipo",
        "grado",
        "grado_nombre",
        "periodo",
        "campo",
        "score",
        "ee",
    ]
)

st.title("Resultados nacionales")

col1, col2 = st.columns(2)

periodos = nacional.get_column("periodo").unique()
with col1:
    periodo = st.selectbox("Año", options=periodos)
nacional_periodo = nacional.filter(pl.col("periodo") == periodo)

grados = nacional_periodo.get_column("grado_nombre").unique()
with col2:
    grado = st.selectbox("Asignatura", options=grados)
nacional_grado = nacional_periodo.filter(pl.col("grado_nombre") == grado)

campos = nacional_grado.get_column("campo").unique()

for campo in campos:
    st.markdown(f"## {campo}")
    nacional_campo = nacional_grado.filter(pl.col("campo") == campo)
    plot = go.Figure(
        data=go.Scatter(
            x=nacional_campo.get_column("tipo"),
            y=nacional_campo.get_column("score"),
            text=nacional_campo.get_column("score").round(2),
            textposition="middle right",
            mode="markers+text",
            error_y=dict(
                type="data",
                array=nacional_campo["ee"],
                visible=True,
            ),
        )
    )
    st.plotly_chart(plot, key=f"{periodo}{grado}{campo}")
