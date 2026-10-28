"""Reto final: extracción, validación y exportación reproducible del dataset de clientes.

Uso (desde la carpeta del proyecto, con el entorno mision4 activado):
    python pipeline.py
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Backend sin ventanas: el gráfico solo se guarda en archivo
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
from dotenv import load_dotenv

from validaciones import validar_dataset

BASE = Path(__file__).resolve().parent
RUTA_ENV = BASE / ".env"
RUTA_CONSULTA = BASE / "consulta_dataset.sql"
CARPETA_SALIDAS = BASE / "salidas"


def leer_configuracion():
    """Lee los datos de conexión desde .env (sin credenciales en el código)."""
    load_dotenv(RUTA_ENV)
    return {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ["DB_PORT"]),
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "database": os.environ["DB_NAME"],
    }


def extraer_dataset():
    """Ejecuta consulta_dataset.sql en MySQL.

    Devuelve el DataFrame, los ids de la tabla clientes (para la cobertura)
    y el número de operaciones con importe NULL (control previo a la agregación).
    """
    config = leer_configuracion()
    consulta = RUTA_CONSULTA.read_text(encoding="utf-8").strip().rstrip(";")

    conexion = None
    cursor = None
    try:
        conexion = mysql.connector.connect(**config)
        cursor = conexion.cursor()

        cursor.execute("SELECT COUNT(*) FROM operaciones WHERE importe IS NULL")
        importes_nulos = cursor.fetchone()[0]

        cursor.execute("SELECT id_cliente FROM clientes")
        ids_clientes = {fila[0] for fila in cursor.fetchall()}

        cursor.execute(consulta)
        filas = cursor.fetchall()
        columnas = [dato[0] for dato in cursor.description]
    finally:
        # Liberación de recursos garantizada, incluso si falla la conexión o la consulta
        if cursor is not None:
            cursor.close()
        if conexion is not None:
            conexion.close()

    return pd.DataFrame(filas, columns=columnas), ids_clientes, importes_nulos


def guardar_informe(informe, carpeta):
    """Escribe informe_validacion.json en la carpeta de la ejecución."""
    ruta = carpeta / "informe_validacion.json"
    ruta.write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta


def exportar_dataset(df, ruta):
    """Guarda el dataset validado en CSV, sin índice."""
    df.to_csv(ruta, index=False)


def generar_grafico(df, ruta):
    """Guarda un gráfico de barras con el gasto medio por situación de abandono."""
    datos = df.copy()
    datos["gasto_total"] = datos["gasto_total"].astype(float)
    medias = (
        datos.groupby("abandono")["gasto_total"].mean()
        .rename(index={0: "Permanece", 1: "Abandona"})
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(medias.index, medias.values, color=["#4C72B0", "#DD8452"])
    for posicion, valor in enumerate(medias.values):
        ax.text(posicion, valor, f"{valor:.2f} €", ha="center", va="bottom")
    ax.set_title("Gasto medio por situación de abandono")
    ax.set_xlabel("Situación del cliente")
    ax.set_ylabel("Gasto medio (€)")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def main():
    """Coordina el proceso: extraer -> validar -> informe -> (solo si es válido) CSV y gráfico."""
    # Carpeta nueva por ejecución: evita confundir resultados anteriores con los actuales
    carpeta = CARPETA_SALIDAS / datetime.now().strftime("ejecucion_%Y%m%d_%H%M%S")
    carpeta.mkdir(parents=True)
    print("Carpeta de esta ejecución:", carpeta.relative_to(BASE))

    try:
        df, ids_clientes, importes_nulos = extraer_dataset()
    except mysql.connector.Error as error:
        # Si la extracción falla, se deja constancia en el informe y se detiene el proceso
        informe = {"valido": False, "error_extraccion": f"{error.errno} - {error.msg}"}
        guardar_informe(informe, carpeta)
        sys.exit(f"Error de MySQL: {error.errno} - {error.msg}. Informe guardado; proceso detenido.")

    print(f"Extracción: {df.shape[0]} filas x {df.shape[1]} columnas")

    informe = validar_dataset(df, ids_esperados=ids_clientes)

    # Importes NULL en operaciones: dato desconocido que SUM/AVG ocultarían
    if importes_nulos > 0:
        informe["incidencias"].append({
            "campo": "importe (operaciones)",
            "regla": "Sin importes NULL antes de agregar",
            "filas": [], "ids": [], "evidencia": [importes_nulos],
            "accion": "Detener: revisar en origen; no rellenar con 0",
        })
        informe["num_incidencias"] = len(informe["incidencias"])
        informe["valido"] = False

    informe["origen"] = f"MySQL - base {os.getenv('DB_NAME')}"
    informe["fecha_ejecucion"] = datetime.now().isoformat(timespec="seconds")

    # El informe se guarda siempre, también cuando la validación falla
    ruta_informe = guardar_informe(informe, carpeta)
    print("Informe guardado:", ruta_informe.relative_to(BASE))

    if not informe["valido"]:
        sys.exit(
            f"Dataset NO válido ({informe['num_incidencias']} incidencias). "
            "Exportación bloqueada: no se generan CSV ni PNG."
        )

    exportar_dataset(df, carpeta / "dataset_clientes.csv")
    generar_grafico(df, carpeta / "gasto_por_abandono.png")
    print("Dataset válido. Generados: dataset_clientes.csv y gasto_por_abandono.png")


if __name__ == "__main__":
    main()