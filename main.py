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
planea_score = pl.read_parquet(ruta.format(m="score_nacional"))
planea_score_ent = pl.read_parquet(ruta.format(m="score_entidad"))
planea_logro = pl.read_parquet(ruta.format(m="logro_nacional"))
planea_logro_ent = pl.read_parquet(ruta.format(m="logro_entidad"))

nacional_score = planea_score.filter(pl.col("subpoblacion") == "Nacional")
nacional_logro = planea_logro.filter(pl.col("subpoblacion") == "Nacional")

### Streamlit ###
st.set_page_config(
    page_title="INEE - Resultados de evaluaciones del aprendizaje",
    page_icon="✅",
    layout="wide",
)

st.title("INEE - Resultados de evaluaciones del aprendizaje")
st.markdown("## PLANEA 2015-2018")
st.image("img/planea.png", width=500)

col_texto_1, col_texto_2 = st.columns(2)

with col_texto_1:
    """
    A continuación, se presentan los principales resultados de las aplicaciones del Plan nacional de evaluación de los aprendizajes (PLANEA) del 2015 al 2018 realizadas por el Instituto Nacional para la Evaluación de la Educación (INEE) de México.
    
    Estas evaluaciones fueron diseñadas para devolver resultados sobre el estado del aprendizaje de las y los estudiantes de obligatoria a nivel de sistema educativo. Siguieron un esquema de aplicación escalonado, en el que diferentes grados escolares y campos de conocimiento o asignaturas fueron evaluados en distintos años, por ello no todos están representados en cada una de las aplicaciones.
    
    Las bases de datos de estas evaluaciones pueden ser encontradas [en este enlace](https://drive.google.com/drive/u/0/folders/1BfdafxB3ehjZRRf80c90Y-XQusN9N85K).
    
    """
with col_texto_2:
    """
    Los resultados de las y los estudiantes fueron expresados como un puntaje estandarizado con una media igual a 500 y una desviación estándar igual a 100, así como en cuatro niveles de logro:

    * **Nivel I.** Los estudiantes que se ubican en este nivel obtienen puntuaciones que representan un logro insuficiente de los aprendizajes clave del currículum, lo que
    refleja carencias fundamentales que dificultarán el aprendizaje futuro.
    * **Nivel II.** Los estudiantes que se ubican en este nivel tienen un logro apenas indispensable de los aprendizajes clave del currículum.
    * **Nivel III.** Los estudiantes que se ubican en este nivel tienen un logro satisfactorio de los aprendizajes clave del currículum.
    * **Nivel IV.** Los estudiantes que se ubican en este nivel tienen un logro sobresaliente de los aprendizajes clave del currículum.
    """

tab_nacional, tab_entidad = st.tabs(["Nacional", "Entidades"])
with tab_nacional:
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
                line_color=COLOR_LINEA,
                showlegend=True,
            )
            score_plot.add_trace(
                go.Scatter(
                    x=score_campo.sort("tipo").get_column("tipo"),
                    y=score_campo.sort("tipo").get_column("score"),
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
                        marker=dict(color=COLOR_BARRA[nivel]),
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

###

with tab_entidad:
    col_sel_ent_1, col_sel_ent_2 = st.columns(2)
    with col_sel_ent_1:
        periodos_ent = (
            planea_score_ent.sort("periodo")
            .get_column("periodo")
            .unique(maintain_order=True)
        )
        periodo_ent = st.selectbox(
            "Año", options=periodos_ent, index=0, key="periodo_ent"
        )
        score_periodo_ent = planea_score_ent.filter(pl.col("periodo") == periodo_ent)
        logro_periodo_ent = planea_logro_ent.filter(pl.col("periodo") == periodo_ent)

    with col_sel_ent_2:
        grados_ent = (
            score_periodo_ent.sort("grado")
            .get_column("grado_nombre")
            .unique(maintain_order=True)
        )
        grado_ent = st.selectbox("Grado", options=grados_ent, index=0, key="grado_ent")
        score_grado_ent = score_periodo_ent.filter(pl.col("grado_nombre") == grado_ent)
        logro_grado_ent = logro_periodo_ent.filter(pl.col("grado_nombre") == grado_ent)
        
    campos_ent = score_grado_ent.sort("campo").get_column("campo").unique(maintain_order=True)
    
    for campo_ent in campos_ent:
        st.markdown(f"## {campo_ent}")
        score_campo_ent = score_grado_ent.filter(pl.col("campo") == campo_ent)
        logro_campo_ent = logro_grado_ent.filter(pl.col("campo") == campo_ent)
        
        col_plot_ent_1, col_plot_ent_2 = st.columns(2, gap="large")
        
        with col_plot_ent_1:
            st. markdown("### Puntaje")
            x_score = score_campo_ent.sort("entidad", descending=True).get_column("puntaje")
            y_ent = score_campo_ent.sort("entidad", descending=True).get_column("entidad")
            text_ent = score_campo_ent.sort("entidad", descending=True).get_column("puntaje").round(2)
            ee_ent = score_campo_ent.sort("entidad", descending=True).get_column("ee")
            score_plot_ent = go.Figure()
            score_plot_ent.add_trace(
                go.Scatter(
                    x=x_score,
                    y=y_ent,
                    name="Puntaje",
                    text=text_ent,
                    textposition="top center",
                    marker_color=COLOR_PUNTO,
                    mode="markers+text",
                    error_x=dict(
                        type="data",
                        array=ee_ent,
                        visible=True,
                    )
                )
            )
            score_plot_ent.update_layout(
                margin=MARGENES,
                xaxis_title="Puntaje",
                yaxis_title="Entidades",
                height=650,
            )
            score_ent = score_campo_ent.select(COLS_SCORE_ENT)
            score_ent.columns = COLS_SCORE_NOMBRE_ENT
            st.plotly_chart(score_plot_ent, key=f"{periodo_ent}{grado_ent}{campo_ent}_score_ent")
            st.dataframe(score_ent.to_pandas().set_index("Aplicación"))
        
        with col_plot_ent_2:
            st.markdown("### Niveles de logro")
            #logro_sorted = logro_campo_ent.sort(["entidad", "nivel"])
            
            niveles_ent = logro_campo_ent.sort("nivel").get_column("nivel").unique(maintain_order=True)
            plot_logro_ent = go.Figure()
            for nivel in niveles_ent:
                logro_nivel_ent = logro_campo_ent.sort("entidad", descending=True).filter(pl.col("nivel") == nivel)
                plot_logro_ent.add_trace(
                    go.Bar(
                        name=nivel,
                        x=logro_nivel_ent.get_column("porcentaje"),
                        y=logro_nivel_ent.get_column("entidad"),
                        text=logro_nivel_ent["porcentaje"],
                        marker=dict(color=COLOR_BARRA[nivel]), orientation="h",
                        
                    )
                )
            plot_logro_ent.update_layout(
                barmode="stack",
                margin=MARGENES,
                xaxis_title="Porcentaje",
                yaxis_title="Entidades",
                height=650,
            )
            
            logro_df_ent = logro_campo_ent.select(COLS_LOGRO_ENT)
            logro_df_ent.columns = COLS_LOGRO_NOMBRE_ENT
            logro_pivot_ent = logro_df_ent.pivot(
                on="Nivel",
                values="Porcentaje",
                index=["Aplicación", "Grado", "Campo", "Entidad"]
            )
            st.plotly_chart(plot_logro_ent, key=f"{periodo_ent}{grado_ent}{campo_ent}_logro_ent")
            st.dataframe(logro_pivot_ent.to_pandas().set_index("Aplicación"))

