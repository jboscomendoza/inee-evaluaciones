import streamlit as st
import polars as pl
import helper as hl
import plotly.graph_objects as go

st.set_page_config(
    page_title="INEE - PLANEA 2015-2018 - Resultados Nacionales",
    page_icon="✅",
    layout="wide",
)

ruta = "data/PLANEA_{m}.parquet"
score = pl.read_parquet(ruta.format(m="score_nacional"))
logro = pl.read_parquet(ruta.format(m="logro_nacional"))


st.title("PLANEA 2015-2018 - Resultados nacionales")
st.image("img/planea.png", width=500)

col_select_1, col_select_2 = st.columns(2)
with col_select_1:
    periodos = score.get_column("periodo").unique()
    periodo = st.selectbox("Año", options=periodos, index=0)
    grados = (
        score.filter(pl.col("periodo") == periodo)
        .get_column("grado_nombre")
        .unique(maintain_order=True)
    )

    orden_score = st.selectbox(
        "Ordenar gráfico de puntaje por:",
        options=["Tipo de escuela", "Puntaje"],
        index=0,
    )

with col_select_2:
    grado = st.selectbox("Grado", options=grados, index=0)
    score_grado = score.filter(
        pl.col("periodo") == periodo, pl.col("grado_nombre") == grado
    )
    logro_grado = logro.filter(
        pl.col("periodo") == periodo, pl.col("grado_nombre") == grado
    )

    orden_logro = st.selectbox(
        "Ordenar gráfico de niveles de logro por:",
        options=["Tipo de escuela", "Nivel 1", "Nivel 2", "Nivel 3", "Nivel 4"],
        index=0,
    )

campos = score_grado.sort("campo").get_column("campo").unique(maintain_order=True)

if orden_score == "Tipo de escuela":
    col_orden_score = "tipo"
else:
    col_orden_score = "score"

for campo in campos:
    st.markdown(f"## {campo}")
    score_campo = score_grado.sort(col_orden_score, descending=True).filter(
        pl.col("campo") == campo
    )
    logro_campo = logro_grado.sort("tipo", descending=True).filter(
        pl.col("campo") == campo
    )

    col_plot_1, col_plot_2 = st.columns(2, gap="large")
    with col_plot_1:
        st.markdown("### Puntaje")

        score_nacional = score_campo.filter(pl.col("tipo") == "Nacional")["score"][0]
        score = score_campo.get_column("score")
        tipo = score_campo.get_column("tipo")
        ee = score_campo.get_column("ee") * 1.96

        score_plot = hl.get_score_plot(score, tipo, ee, score_nacional=score_nacional)

        cols_score = hl.get_cols("score", "nacional")
        cols_score_titulo = hl.get_cols("score", "nacional", True)
        score_df = score_campo.select(cols_score).sort("tipo")
        score_df.columns = cols_score_titulo

        st.plotly_chart(score_plot, key=f"{periodo}{grado}{campo}_score")
        st.dataframe(score_df.to_pandas().set_index("Aplicación"))

    with col_plot_2:
        st.markdown("### Niveles de logro")

        if orden_logro != "Tipo de escuela":
            orden_enum = (
                logro_campo.with_columns(pl.col("tipo").cast(pl.String()))
                .filter(pl.col("nivel") == orden_logro)
                .sort("porcentaje")
                .get_column("tipo")
                .unique(maintain_order=True)
            )
            logro_campo = logro_campo.with_columns(
                pl.col("tipo").cast(pl.Enum(orden_enum))
            ).sort("tipo")

        plot_logro = hl.get_logro_plot(logro_campo, "tipo")

        cols_logro = hl.get_cols("logro", "nacional")
        cols_logro_titulo = hl.get_cols("logro", "nacional", True)
        logro_df = logro_campo.select(cols_logro).sort("tipo")
        logro_df.columns = cols_logro_titulo
        logro_pivot = logro_df.sort("Nivel").pivot(
            on="Nivel",
            values="Porcentaje",
            index=["Aplicación", "Grado", "Campo", "Tipo"],
        )

        st.plotly_chart(plot_logro, key=f"{periodo}{grado}{campo}_logro")
        st.dataframe(logro_pivot.to_pandas().set_index("Aplicación"))
