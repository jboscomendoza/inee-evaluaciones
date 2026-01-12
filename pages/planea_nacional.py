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
score = pl.read_parquet(ruta.format(m="score_nacional")).filter(
    pl.col("subpoblacion") == "Nacional"
)
logro = pl.read_parquet(ruta.format(m="logro_nacional")).filter(
    pl.col("subpoblacion") == "Nacional"
)


st.title("PLANEA 2015-2018 - Resultados nacionales")
st.image("img/planea.png", width=500)

col_select_1, col_select_2 = st.columns(2)
with col_select_1:
    periodos = score.get_column("periodo").unique()
    periodo = st.selectbox("Año", options=periodos, index=0)
    score_periodo = score.filter(pl.col("periodo") == periodo)
    logro_periodo = logro.filter(pl.col("periodo") == periodo)

with col_select_2:
    grados = score_periodo.get_column("grado_nombre").unique()
    grado = st.selectbox("Grado", options=grados, index=0)
    score_grado = score_periodo.filter(pl.col("grado_nombre") == grado)
    logro_grado = logro_periodo.filter(pl.col("grado_nombre") == grado)

campos = score_grado.sort("campo").get_column("campo").unique(maintain_order=True)

for campo in campos:
    st.markdown(f"## {campo}")
    score_campo = score_grado.sort("tipo", descending=True).filter(
        pl.col("campo") == campo
    )
    logro_campo = logro_grado.sort("tipo", descending=True).filter(
        pl.col("campo") == campo
    )

    col_plot_1, col_plot_2 = st.columns(2, gap="large")
    with col_plot_1:
        score_nacional = score_campo.filter(pl.col("tipo") == "Nacional")["score"][0]

        st.markdown("### Puntaje")

        score = score_campo.get_column("score")
        tipo = score_campo.get_column("tipo")
        ee = score_campo.get_column("ee") * 1.96
        
        score_plot = go.Figure()
        score_plot.add_vline(
            x=score_nacional,
            name="Media nacional",
            line_color=hl.COLOR_LINEA,
            showlegend=True,
        )
        score_plot.add_trace(
            go.Scatter(
                x=score,
                y=tipo,
                name="Puntaje",
                text=score.round(2),
                textposition="top center",
                marker_color=hl.COLOR_PUNTO,
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
            yaxis_title="Nacional y tipos de escuela",
            margin=hl.MARGENES,
        )
        cols_score = hl.get_cols("score", "nacional")
        cols_score_titulo = hl.get_cols("score", "nacional", True)
        score_df = score_campo.select(cols_score).sort("tipo")
        score_df.columns = cols_score_titulo
        st.plotly_chart(score_plot, key=f"{periodo}{grado}{campo}_score")
        st.dataframe(score_df.to_pandas().set_index("Aplicación"))

    with col_plot_2:
        st.markdown("### Niveles de logro")

        niveles = (
            logro_campo.sort("nivel").get_column("nivel").unique(maintain_order=True)
        )

        plot_logro = go.Figure()
        for nivel in niveles:
            logro_nivel = logro_campo.filter(pl.col("nivel") == nivel)
            porcentaje = logro_nivel.get_column("porcentaje")
            tipo = logro_nivel.get_column("tipo")

            plot_logro.add_trace(
                go.Bar(
                    name=nivel,
                    x=porcentaje,
                    y=tipo,
                    text=porcentaje,
                    marker=dict(color=hl.COLOR_BARRA[nivel]),
                    orientation="h",
                )
            )
        plot_logro.update_layout(
            barmode="stack",
            margin=hl.MARGENES,
            xaxis_title="Porcentaje por nivel de logro",
            yaxis_title="Nacional y tipos de escuela",
        )

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
