COLOR_BARRA = {
    "Nivel 1": "#f3722c",
    "Nivel 2": "#f9c74f",
    "Nivel 3": "#90be6d",
    "Nivel 4": "#577590",
}

COLOR_LINEA = "#815ac0"

COLOR_PUNTO = "#4D9DE0"

MARGENES = dict(t=30, b=40)

def get_cols(metrica: str, grupo: str, titulo: bool = False) -> list:
    """
    Devuelve una lista con nombres de columnas.

    :param metrica: Uno de "score" o "logro".
    :type metrica: str
    :param grupo: Uno de "nacional" o "entidad".
    :type grupo: str
    :param titulo: Si debe devolver los nombres con formato de título.
    :type titulo: bool
    :return: Una lista con nombres de columnas.
    :rtype: list
    """
    if grupo == "nacional":
        col_grupo = "tipo"
    elif grupo == "entidad":
        col_grupo = "entidad"
    if metrica == "score" and titulo:
        cols = [
            "Aplicación",
            "Grado",
            "Campo",
            col_grupo.title(),
            "Puntaje",
            "Error estándar",
            "Escuelas",
            "Estudiantes",
        ]
    elif metrica == "score":
        cols = [
            "periodo",
            "grado_nombre",
            "campo",
            col_grupo,
            "score",
            "ee",
            "escuelas",
            "estudiantes",
        ]
    elif metrica == "logro" and titulo:
        cols = [
            "Aplicación",
            "Grado",
            "Campo",
            col_grupo.title(),
            "Nivel",
            "Porcentaje",
            "Escuelas",
            "Estudiantes",
        ]
    elif metrica == "logro":
        cols = [
            "periodo",
            "grado_nombre",
            "campo",
            col_grupo,
            "nivel",
            "porcentaje",
            "escuelas",
            "estudiantes",
        ]
    return cols
