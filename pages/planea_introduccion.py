import streamlit as st

### Streamlit ###
st.set_page_config(
    page_title="INEE - PLANEA 2015-2018 Introducción",
    page_icon="✅",
    layout="wide",
)

st.title("PLANEA 2015-2018 - Introducción")
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
