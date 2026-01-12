import streamlit as st
import polars as pl
import plotly.graph_objects as go
import helper as hl

st.set_page_config(
    page_title="INEE - PLANEA 2015-2018 - Resultados estatales",
    page_icon="✅",
    layout="wide",
)

ALTURA = 730

ruta = "data/PLANEA_{m}.parquet"
score = pl.read_parquet(ruta.format(m="score_entidad"))
logro = pl.read_parquet(ruta.format(m="logro_entidad"))

st.title("PLANEA 2015-2018 - Resultados por entidad")
st.image("img/planea.png", width=500)

col_sel_1, col_sel_2 = st.columns(2)
with col_sel_1:
    periodos = score.sort("periodo").get_column("periodo").unique(maintain_order=True)
    periodo = st.selectbox("Año", options=periodos, index=0, key="periodo")
    score_periodo = score.filter(pl.col("periodo") == periodo)
    logro_periodo = logro.filter(pl.col("periodo") == periodo)

with col_sel_2:
    grados = (
        score_periodo.sort("grado")
        .get_column("grado_nombre")
        .unique(maintain_order=True)
    )
    grado = st.selectbox("Grado", options=grados, index=0)
    score_grado = score_periodo.filter(pl.col("grado_nombre") == grado)
    logro_grado = logro_periodo.filter(pl.col("grado_nombre") == grado)

campos = score_grado.sort("campo").get_column("campo").unique(maintain_order=True)

for campo in campos:
    st.markdown(f"## {campo}")
    score_campo = score_grado.sort("entidad", descending=True).filter(
        pl.col("campo") == campo
    )
    logro_campo = logro_grado.sort("entidad", descending=True).filter(
        pl.col("campo") == campo
    )

    col_plot_ent_1, col_plot_ent_2 = st.columns(2, gap="large")

    with col_plot_ent_1:
        st.markdown("### Puntaje")

        score = score_campo.get_column("score")
        entidad = score_campo.get_column("entidad")
        ee = score_campo.get_column("ee") * 1.96

        score_plot = hl.get_score_plot(score, entidad, ee)

        cols_score = hl.get_cols("score", "entidad")
        cols_score_titulo = hl.get_cols("score", "entidad", True)
        score = score_campo.select(cols_score).sort("entidad")
        score.columns = cols_score_titulo
        st.plotly_chart(score_plot, key=f"{periodo}{grado}{campo}_score")
        st.dataframe(score.to_pandas().set_index("Aplicación"))

    with col_plot_ent_2:
        st.markdown("### Niveles de logro")
        niveles = (
            logro_campo.sort("nivel").get_column("nivel").unique(maintain_order=True)
        )
        plot_logro = go.Figure()
        for nivel in niveles:
            logro_nivel = logro_campo.filter(pl.col("nivel") == nivel)
            porcentaje = logro_nivel.get_column("porcentaje")
            entidad = logro_nivel.get_column("entidad")

            plot_logro.add_trace(
                go.Bar(
                    name=nivel,
                    x=porcentaje,
                    y=entidad,
                    text=porcentaje,
                    marker=dict(color=hl.COLOR_BARRA[nivel]),
                    orientation="h",
                )
            )
        plot_logro.update_layout(
            barmode="stack",
            margin=hl.MARGENES,
            xaxis_title="Porcentaje por nivel logro",
            yaxis_title="Entidades",
            height=ALTURA,
        )

        cols_logro = hl.get_cols("logro", "entidad")
        cols_logro_titulo = hl.get_cols("logro", "entidad", True)
        logro_df = logro_campo.select(cols_logro)
        logro_df.columns = cols_logro_titulo
        logro_pivot = logro_df.pivot(
            on="Nivel",
            values="Porcentaje",
            index=["Aplicación", "Grado", "Campo", "Entidad"],
        ).sort("Entidad")
        st.plotly_chart(plot_logro, key=f"{periodo}{grado}{campo}_logro")
        st.dataframe(logro_pivot.to_pandas().set_index("Aplicación"))
