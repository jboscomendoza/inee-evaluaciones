COLOR_BARRA = {
    "Nivel 1": "#f3722c",
    "Nivel 2": "#f9c74f",
    "Nivel 3": "#90be6d",
    "Nivel 4": "#577590",
}

COLOR_LINEA = "#815ac0"

COLOR_PUNTO = "#4D9DE0"

def get_cols(metrica: str, grupo: str) -> list:
    """
    Devuelve una lista con nombres de columnas

    :param metrica: Uno de "score" o "logro".
    :type metrica: str
    :param grupo: Description
    :type grupo: Uno de "nacional" o "entidades".
    :return: Lista con nombres de columnas.
    :rtype: list
    """
    if metrica == "score":
        cols = [
            "periodo",
            "grado_nombre",
            "campo",
            "tipo",
            "score",
            "ee",
            "escuelas",
            "estudiantes",
        ]
    elif metrica == "logro":
        cols = [
            "periodo",
            "grado_nombre",
            "campo",
            "tipo",
            "nivel",
            "porcentaje",
            "escuelas",
            "estudiantes",
        ]
    return cols
