"""Reto 1 y Reto 4. Completa las funciones sin cambiar el dato recibido."""


def validar_cliente(cliente):
    """Revisa un cliente y devuelve una lista con TODOS sus errores."""
    incidencias = []  # lista vacía donde iremos anotando errores

    # Regla 1: el id debe existir y no ser None
    if cliente.get("id_cliente") is None:
        incidencias.append("Falta id_cliente")

    # Regla 2: la antigüedad no puede ser negativa
    if cliente["antiguedad_meses"] < 0:
        incidencias.append("Antigüedad negativa")

    # Regla 3: abandono solo puede ser 0 o 1
    if cliente["abandono"] not in (0, 1):
        incidencias.append("Abandono debe ser 0 o 1")

    return incidencias  # se devuelve al final, con todos los errores


def validar_dataset(df, ids_esperados=None):
    # Devuelve un informe serializable como JSON:
    # valido, filas, columnas, incidencias (regla, campo, filas, accion).
    # Además de tipos/rangos, comprueba unicidad y cobertura de clientes.
    raise NotImplementedError("Completa el reto 4")