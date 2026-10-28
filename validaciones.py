"""Reto 1 y Reto 4. Funciones de validación de clientes y del dataset."""
import numpy as np
import pandas as pd

# Contrato del dataset: seis columnas, en este orden
COLUMNAS_ESPERADAS = [
    "id_cliente", "antiguedad_meses", "num_operaciones",
    "gasto_total", "ticket_medio", "abandono",
]
COLUMNAS_ENTERAS = ["id_cliente", "antiguedad_meses", "num_operaciones", "abandono"]


def validar_cliente(cliente):
    """Revisa un cliente y devuelve una lista con TODOS sus errores."""
    incidencias = []  # Acumula todas las incidencias detectadas

    # Regla 1: el id debe existir y no ser None
    if cliente.get("id_cliente") is None:
        incidencias.append("Falta id_cliente")

    # Regla 2: la antigüedad no puede ser negativa
    if cliente["antiguedad_meses"] < 0:
        incidencias.append("Antigüedad negativa")

    # Regla 3: abandono solo puede ser 0 o 1
    if cliente["abandono"] not in (0, 1):
        incidencias.append("Abandono debe ser 0 o 1")

    return incidencias


def _valor_legible(valor):
    """Convierte un valor a un tipo serializable en JSON (None, int, float o str)."""
    if pd.isna(valor):
        return None
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    return int(numero) if numero.is_integer() else numero


def _registrar(incidencias, original, mascara, campo, regla, accion):
    """Añade una incidencia con posiciones, ids y valores afectados si la máscara marca filas."""
    if mascara.any():
        incidencias.append({
            "campo": campo,
            "regla": regla,
            "filas": [int(i) for i in original.index[mascara]],
            "ids": [_valor_legible(v) for v in original.loc[mascara, "id_cliente"]],
            "evidencia": [_valor_legible(v) for v in original.loc[mascara, campo]],
            "accion": accion,
        })


def validar_dataset(df, ids_esperados=None):
    """Valida el dataset contra el contrato y devuelve un informe serializable en JSON.

    No modifica el DataFrame recibido: trabaja sobre una copia.
    Las posiciones de 'filas' empiezan en 0 (primera fila de datos).
    """
    original = df.reset_index(drop=True).copy()
    incidencias = []

    # 1. Esquema: mismas columnas y en el mismo orden
    columnas = original.columns.tolist()
    if columnas != COLUMNAS_ESPERADAS:
        incidencias.append({
            "campo": "esquema",
            "regla": "Seis columnas del contrato en el orden acordado",
            "filas": [],
            "ids": [],
            "evidencia": columnas,
            "accion": "Detener: corregir la consulta de extracción",
        })
        if set(COLUMNAS_ESPERADAS) - set(columnas):
            # Sin todas las columnas no se pueden aplicar el resto de reglas
            return _crear_informe(original, incidencias)

    # Conversión a numérico en una copia (MySQL DECIMAL llega como object/Decimal)
    numerico = original[COLUMNAS_ESPERADAS].apply(pd.to_numeric, errors="coerce")

    for campo in COLUMNAS_ESPERADAS:
        serie = numerico[campo]

        # 2. Campos obligatorios sin valores ausentes
        _registrar(incidencias, original, original[campo].isna(), campo,
                   "Valor ausente en campo obligatorio",
                   "Detener: revisar en origen; no rellenar con 0")

        # 3. Valores numéricos y finitos
        _registrar(incidencias, original, serie.isna() & original[campo].notna(), campo,
                   "Valor no numérico", "Detener: corregir en origen")
        _registrar(incidencias, original, np.isinf(serie), campo,
                   "Valor no finito", "Detener: corregir en origen")

        valido_num = serie.notna() & np.isfinite(serie)

        # 4. Enteros donde procede
        if campo in COLUMNAS_ENTERAS:
            _registrar(incidencias, original, valido_num & (serie % 1 != 0), campo,
                       "Debe ser un número entero", "Rechazar: revisar en origen")

        # 5. Rangos: id positivo y resto no negativos
        if campo == "id_cliente":
            _registrar(incidencias, original, valido_num & (serie <= 0), campo,
                       "id_cliente debe ser positivo", "Detener: revisar en origen")
        elif campo != "abandono":
            _registrar(incidencias, original, valido_num & (serie < 0), campo,
                       "No puede ser negativo", "Rechazar: revisar en origen")

    # 6. Etiqueta de abandono: solo 0 o 1
    abandono = numerico["abandono"]
    _registrar(incidencias, original, abandono.notna() & ~abandono.isin([0, 1]), "abandono",
               "Abandono debe ser 0 o 1", "Rechazar: etiqueta no válida")

    # 7. Unicidad: una fila por cliente
    ids = numerico["id_cliente"]
    _registrar(incidencias, original, ids.notna() & ids.duplicated(keep=False), "id_cliente",
               "id_cliente duplicado (una fila por cliente)",
               "Detener: revisar JOIN/GROUP BY; no usar drop_duplicates")

    # 8. Cobertura frente a los ids de referencia de la tabla clientes
    if ids_esperados is not None:
        presentes = {int(v) for v in ids.dropna()}
        esperados = {int(v) for v in ids_esperados}
        faltan = sorted(esperados - presentes)
        sobran = sorted(presentes - esperados)
        if faltan:
            incidencias.append({
                "campo": "id_cliente", "regla": "Cobertura: faltan clientes de la referencia",
                "filas": [], "ids": faltan, "evidencia": [],
                "accion": "Detener: revisar LEFT JOIN y filtros",
            })
        if sobran:
            incidencias.append({
                "campo": "id_cliente", "regla": "Cobertura: ids que no están en la referencia",
                "filas": [], "ids": sobran, "evidencia": [],
                "accion": "Detener: revisar origen de los datos",
            })

    return _crear_informe(original, incidencias)


def _crear_informe(original, incidencias):
    """Construye el informe final de validación."""
    filas_afectadas = sorted({fila for inc in incidencias for fila in inc["filas"]})
    return {
        "valido": len(incidencias) == 0,
        "filas": int(len(original)),
        "columnas": original.columns.tolist(),
        "num_incidencias": len(incidencias),
        "filas_afectadas": filas_afectadas,
        "incidencias": incidencias,
    }