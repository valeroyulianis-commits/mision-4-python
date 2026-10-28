"""Reto final: completa este script y ejecútalo desde una terminal nueva."""
from pathlib import Path
from validaciones import validar_dataset

BASE = Path(__file__).resolve().parent


def extraer_dataset():
    # Lee .env. Conecta a MySQL. Comprueba importes NULL en operaciones.
    # Ejecuta consulta_dataset.sql. Recupera también los ids de clientes.
    # Cierra cursor y conexión en finally, incluso si hay una excepción.
    raise NotImplementedError("Completa la extracción")


def main():
    # Crea una carpeta nueva para cada ejecución en salidas/.
    # Extrae -> valida -> escribe informe (también si falla).
    # Solo si el informe es válido: exporta CSV y gráfico.
    raise NotImplementedError("Completa el proceso")


if __name__ == "__main__":
    main()
