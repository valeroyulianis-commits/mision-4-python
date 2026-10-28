# Misión 4 · Del dato al proceso

Proceso Python reproducible que extrae el dataset de clientes desde MySQL (base `ai_customer` de la Misión 3), lo valida contra el contrato acordado y, solo si es válido, exporta el CSV y un gráfico. Proyecto *AI Customer Intelligence*: en esta misión se preparan los datos para estudiar el abandono, sin entrenar un modelo.

**Autoras:** Yulianis Valero y Yuleimis Valero · Máster en IA Aplicada, Universidad Europea

## Estructura

| Archivo | Contenido |
|---|---|
| `mision_4.ipynb` | Exploración: retos 1–4 y microreto de pandas/matplotlib |
| `validaciones.py` | `validar_cliente()` (Reto 1) y `validar_dataset()` (Reto 4) |
| `pipeline.py` | Proceso completo: extraer → validar → informe → CSV y gráfico |
| `consulta_dataset.sql` | Consulta de extracción (LEFT JOIN + agregaciones, una fila por cliente) |
| `datos/` | CSV del kit: referencia (válido) y copia con incidencias (Reto 4) |
| `.env.example` | Plantilla de configuración sin credenciales |
| `requirements.txt` | Dependencias del proyecto |
| `Plantilla_evidencias.md` | Evidencias de cada reto |

## Preparación

1. MySQL Server 8.4 en local con la base `ai_customer` de la Misión 3 (tablas `clientes` y `operaciones`).
2. Crear y activar el entorno (Anaconda PowerShell Prompt, desde esta carpeta):
   ```powershell
   conda create -n mision4 python=3.12 -y
   conda activate mision4
   python -m pip install -r requirements.txt
   python -m ipykernel install --user --name mision4 --display-name "Python (Misión 4)"
   ```
3. Copiar `.env.example` como `.env` y completar el usuario y la contraseña locales de MySQL, con `DB_NAME=ai_customer`.
   `.env` está excluido en `.gitignore`: no se sube al repositorio ni se entrega.
4. Para el notebook: abrir `mision_4.ipynb` en VS Code, seleccionar el kernel **Python (Misión 4)**, hacer *Restart* y *Run All*.

## Ejecución

Desde una terminal nueva, en la carpeta del proyecto y con el entorno activado:

```powershell
conda activate mision4
python pipeline.py
```

Cada ejecución crea una carpeta nueva `salidas/ejecucion_AAAAMMDD_HHMMSS/`:

- **Siempre:** `informe_validacion.json` (resultado de la validación e incidencias).
- **Solo si el dataset es válido:** `dataset_clientes.csv` (sin índice) y `gasto_por_abandono.png`.
- Si la validación falla, el script termina con un mensaje de error y no genera CSV ni PNG.

## Contrato del dataset y reglas de validación

Una fila por cliente, incluidos los clientes sin operaciones. Seis columnas, en este orden:
`id_cliente, antiguedad_meses, num_operaciones, gasto_total, ticket_medio, abandono`.

| Regla | Acción si falla |
|---|---|
| Esquema: seis columnas en el orden acordado | Detener |
| Sin valores ausentes en ninguna columna | Detener; no rellenar con 0 |
| Valores numéricos y finitos | Detener |
| `id_cliente`, `antiguedad_meses`, `num_operaciones` y `abandono` enteros | Rechazar |
| `id_cliente` positivo; el resto, no negativos | Rechazar / Detener |
| `abandono` solo 0 o 1 | Rechazar |
| `id_cliente` único (una fila por cliente) | Detener; no usar `drop_duplicates` |
| Cobertura: mismos ids que la tabla `clientes` | Detener; revisar LEFT JOIN |
| Sin importes NULL en `operaciones` antes de agregar | Detener |

Convención: un cliente sin operaciones tiene `num_operaciones = 0`, `gasto_total = 0` y `ticket_medio = 0`; este último es una convención, no una media calculada. No se corrige ningún dato sin una fuente comprobada.

## Completado antes de entregar

- **Entorno y versión de Python:** Anaconda, entorno `mision4`, Python 3.12.16 (Windows 11, VS Code).
- **Base y origen de los datos:** MySQL local, base `ai_customer` (Misión 3): 30 clientes y 99 operaciones.
- **Comando y ruta de resultados:** `python pipeline.py` → `salidas/ejecucion_AAAAMMDD_HHMMSS/`.
- **Reglas, incidencias y decisiones:**
  - Dataset de MySQL: 30 filas × 6 columnas, 0 incidencias, 0 importes NULL → **válido**.
  - `datos/dataset_con_incidencias.csv`: 9 incidencias → **exportación bloqueada**. No se aplicaron correcciones porque no hay una fuente comprobada para los valores reales.
  - Prueba de error crítico: al cambiar `LEFT JOIN` por `INNER JOIN` se pierden los 4 clientes sin operaciones (7, 14, 21, 28); la regla de cobertura lo detecta, se guarda el informe y no se genera CSV ni PNG.
- **Observación del gráfico:** los clientes que permanecen (21) tienen un gasto medio de 624,49 €, unos 179 € más que los que abandonan (9 clientes, 445,51 €).
- **Limitación:** el grupo de abandono es pequeño (9 clientes) e incluye a los 4 clientes sin operaciones, cuyo gasto de 0 € reduce su media. La mediana muestra lo contrario (586,81 € frente a 525,01 €). Con 30 clientes la diferencia no es concluyente y describe una asociación, no una relación causal.
- **Ayuda de IA y comprobación:** se usó un asistente de IA (Claude) como guía paso a paso y para proponer el código de las funciones. Todo el código se revisó y se verificó ejecutándolo: casos de prueba del inspector (válido, antigüedad negativa, sin id, cliente 104 con dos errores), comparación del recuento y de las cinco primeras filas con MySQL Workbench, validación del dataset correcto y de la copia con incidencias, y ejecución válida y bloqueada del pipeline desde una terminal nueva.