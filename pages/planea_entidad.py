import streamlit as st
import polars as pl
import plotly.graph_objects as go
import helper as hl

ruta = "data/PLANEA_{m}.parquet"
score_ent = pl.read_parquet(ruta.format(m="score_entidad"))
logro_ent = pl.read_parquet(ruta.format(m="logro_entidad"))

col_sel_ent_1, col_sel_ent_2 = st.columns(2)
with col_sel_ent_1:
    periodos_ent = (
        score_ent.sort("periodo").get_column("periodo").unique(maintain_order=True)
    )
    periodo_ent = st.selectbox("Año", options=periodos_ent, index=0, key="periodo_ent")
    score_periodo_ent = score_ent.filter(pl.col("periodo") == periodo_ent)
    logro_periodo_ent = logro_ent.filter(pl.col("periodo") == periodo_ent)

with col_sel_ent_2:
    grados_ent = (
        score_periodo_ent.sort("grado")
        .get_column("grado_nombre")
        .unique(maintain_order=True)
    )
    grado_ent = st.selectbox("Grado", options=grados_ent, index=0, key="grado_ent")
    score_grado_ent = score_periodo_ent.filter(pl.col("grado_nombre") == grado_ent)
    logro_grado_ent = logro_periodo_ent.filter(pl.col("grado_nombre") == grado_ent)

campos_ent = (
    score_grado_ent.sort("campo").get_column("campo").unique(maintain_order=True)
)

for campo_ent in campos_ent:
    st.markdown(f"## {campo_ent}")
    score_campo_ent = score_grado_ent.filter(pl.col("campo") == campo_ent)
    logro_campo_ent = logro_grado_ent.filter(pl.col("campo") == campo_ent)

    col_plot_ent_1, col_plot_ent_2 = st.columns(2, gap="large")

    with col_plot_ent_1:
        st.markdown("### Puntaje")
        x_score = score_campo_ent.sort("entidad", descending=True).get_column("score")
        y_ent = score_campo_ent.sort("entidad", descending=True).get_column("entidad")
        text_ent = (
            score_campo_ent.sort("entidad", descending=True)
            .get_column("score")
            .round(2)
        )
        ee_ent = score_campo_ent.sort("entidad", descending=True).get_column("ee")
        score_plot_ent = go.Figure()
        score_plot_ent.add_trace(
            go.Scatter(
                x=x_score,
                y=y_ent,
                name="score",
                text=text_ent,
                textposition="top center",
                marker_color=hl.COLOR_PUNTO,
                mode="markers+text",
                error_x=dict(
                    type="data",
                    array=ee_ent,
                    visible=True,
                ),
            )
        )
        score_plot_ent.update_layout(
            margin=hl.MARGENES,
            xaxis_title="score",
            yaxis_title="Entidades",
            height=650,
        )
        cols_score = hl.get_cols("score", "entidad")
        cols_score_titulo = hl.get_cols("score", "entidad", True)
        score_ent = score_campo_ent.select(cols_score)
        score_ent.columns = cols_score_titulo
        st.plotly_chart(
            score_plot_ent, key=f"{periodo_ent}{grado_ent}{campo_ent}_score_ent"
        )
        st.dataframe(score_ent.to_pandas().set_index("Aplicación"))

    with col_plot_ent_2:
        st.markdown("### Niveles de logro")
        niveles_ent = (
            logro_campo_ent.sort("nivel")
            .get_column("nivel")
            .unique(maintain_order=True)
        )
        plot_logro_ent = go.Figure()
        for nivel in niveles_ent:
            logro_nivel_ent = logro_campo_ent.sort("entidad", descending=True).filter(
                pl.col("nivel") == nivel
            )
            plot_logro_ent.add_trace(
                go.Bar(
                    name=nivel,
                    x=logro_nivel_ent.get_column("porcentaje"),
                    y=logro_nivel_ent.get_column("entidad"),
                    text=logro_nivel_ent["porcentaje"],
                    marker=dict(color=hl.COLOR_BARRA[nivel]),
                    orientation="h",
                )
            )
        plot_logro_ent.update_layout(
            barmode="stack",
            margin=hl.MARGENES,
            xaxis_title="Porcentaje",
            yaxis_title="Entidades",
            height=650,
        )

        cols_logro = hl.get_cols("logro", "entidad")
        cols_logro_titulo = hl.get_cols("logro", "entidad", True)
        logro_df_ent = logro_campo_ent.select(cols_logro)
        logro_df_ent.columns = cols_logro_titulo
        logro_pivot_ent = logro_df_ent.pivot(
            on="Nivel",
            values="Porcentaje",
            index=["Aplicación", "Grado", "Campo", "Entidad"],
        )
        st.plotly_chart(
            plot_logro_ent, key=f"{periodo_ent}{grado_ent}{campo_ent}_logro_ent"
        )
        st.dataframe(logro_pivot_ent.to_pandas().set_index("Aplicación"))
