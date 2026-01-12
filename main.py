import streamlit as st

pages = {
    "PLANEA": [
        st.Page("pages/planea_introduccion.py", title="Introducción"),
        st.Page("pages/planea_nacional.py", title="Nacional"),
        st.Page("pages/planea_entidad.py", title="Entidades"),
    ]
}

pg = st.navigation(pages)

pg.run()
