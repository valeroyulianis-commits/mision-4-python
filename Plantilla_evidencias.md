# Evidencias · Misión 4

Nombre(s), fecha, grupo y reparto de roles: Yulianis Valero y Yuleimis Valero · 28/10/2026  
Origen de datos (MySQL / CSV de respaldo), base y entorno: MySQL 8.4 local, base `ai_customer` (Misión 3) · Anaconda, entorno `mision4`, Python 3.12.16 · VS Code en Windows 11

## 1. Inspector
Casos: válido → []; antigüedad negativa → un error; cliente 104 con -3 y 2 → dos errores.
- Válido → `[]`
- Antigüedad negativa → `['Antigüedad negativa']`
- Cliente 104 (-3 y 2) → `['Antigüedad negativa', 'Abandono debe ser 0 o 1']`; el diccionario original no se modifica.

Caso id ausente → error: `['Falta id_cliente']`
Nº de clientes con errores en la lista: 1 (el cliente 102 tiene dos mensajes, pero cuenta como un cliente).
Explica por qué no devuelves el resultado tras el primer if: porque `return` termina la función; si estuviera tras el primer `if`, no se revisarían las demás reglas y el cliente 104 mostraría un solo error. Los `if` son independientes (no `elif`) y `return` va al final para devolver todas las incidencias.

## 2. Puente Python–MySQL
Recuento de clientes en Workbench / Python: 30 / 30
Primeras cinco filas (captura sin credenciales): ids 1 a 5 coinciden en Python y Workbench (Cliente 01–05; antigüedad 1, 31, 8, 26, 10).
Error provocado con DB_NAME, diagnóstico y recuperación: con `DB_NAME=ai_customer_inventada` → `Error de MySQL: 1049 - Unknown database 'ai_customer_inventada'`. Causa: la base indicada en `.env` no existe. Solución: restaurar `DB_NAME=ai_customer`, reiniciar el kernel (load_dotenv no sobrescribe variables ya cargadas) y volver a ejecutar → 30 clientes.
Explica dónde se cierran cursor y conexión: en el bloque `finally`, que se ejecuta siempre, también cuando falla la conexión o la consulta. Se comprueba antes que no sean `None`.

## 3. Dataset
Consulta usada y explicación del LEFT JOIN: `consulta_dataset.sql` (clientes LEFT JOIN operaciones, GROUP BY cliente, COUNT/SUM/AVG con COALESCE). El LEFT JOIN conserva todos los clientes, incluso sin operaciones; para ellos `COUNT(o.id_operacion)` da 0 y COALESCE convierte la suma y la media vacías en 0.
shape / tipos / faltantes / duplicados / comparación de ids: (30, 6) · id, antigüedad, num_operaciones y abandono int64; gasto_total y ticket_medio object (DECIMAL de MySQL llega como Decimal) · 0 ausentes · `id_cliente` único: True · mismo conjunto de ids que la tabla clientes: True (30 = 30).
Cliente sin operaciones que se conserva y valores obtenidos: 4 clientes (7, 14, 21, 28) con num_operaciones 0, gasto_total 0.00, ticket_medio 0 y abandono 1. Ejemplo: cliente 7, antigüedad 3 meses.
Cómo detectaste importes desconocidos antes de la agregación: `SELECT COUNT(*) FROM operaciones WHERE importe IS NULL` → 0 (además, la columna `importe` está definida NOT NULL). Se comprueba antes porque SUM y AVG ignoran los NULL y podrían ocultar importes desconocidos.

## 4. Calidad
| Campo | Regla | Filas afectadas (posición e id) | Evidencia | Acción | Resultado |
|---|---|---|---|---|---|
| id_cliente | Valor ausente | 3 / — | vacío | Detener: revisar en origen | Sin resolver |
| antiguedad_meses | Debe ser entero | 8 / 109 | 2.5 | Rechazar | Sin resolver |
| antiguedad_meses | No negativa | 1 / 102 | -4 | Rechazar | Sin resolver |
| num_operaciones | Debe ser entero | 5 / 106 | 1.5 | Rechazar | Sin resolver |
| gasto_total | Valor ausente | 4 / 105 | vacío | Detener; no rellenar con 0 | Sin resolver |
| gasto_total | Valor no numérico | 7 / 108 | "error" | Detener | Sin resolver |
| abandono | Debe ser 0 o 1 | 2 / 103 | 2 | Rechazar | Sin resolver |
| id_cliente | Duplicado | 0 y 12 / 101 | 101 dos veces | Detener; no usar drop_duplicates | Sin resolver |
| id_cliente | Cobertura | — / falta 104 | — | Detener; revisar LEFT JOIN | Sin resolver |

Filas antes / después: 13 / 13 (no se eliminan duplicados ni se rellenan ausentes).
Correcciones verificadas / incidencias sin resolver: 0 / 9 (no hay fuente comprobada para corregir; se detiene la exportación).
Resultado con dataset válido / con dataset incorrecto: MySQL `ai_customer` → válido, 0 incidencias / copia con incidencias → no válido, 9 incidencias en 9 filas (posiciones 0, 1, 2, 3, 4, 5, 7, 8, 12), exportación bloqueada.
Ruta del informe guardado en la ejecución inválida: `salidas/reto4_informe_practica.json` (notebook) y `salidas/ejecucion_20261028_2306xx/informe_validacion.json` (pipeline con INNER JOIN) [verificar nombre exacto de la carpeta].

## 5. Pandas y gráfico
Filtro gasto > 100, columna sin_operaciones y resumen por abandono: 26 de 30 clientes con gasto_total > 100 (máximo: cliente 18, 1.543,91 €) · `sin_operaciones` = True en 4 clientes, todos con abandono 1 (columna creada en una copia; el CSV mantiene las 6 columnas) · Permanece: 21 clientes, media 624,49 €, mediana 525,01 € · Abandona: 9 clientes, media 445,51 €, mediana 586,81 €.
Título, ejes y unidad del gráfico: "Gasto medio por situación de abandono" · eje X: Situación del cliente · eje Y: Gasto medio (€).
Una observación sustentada en valores: los clientes que permanecen gastan de media 624,49 €, unos 179 € más que los que abandonan (445,51 €).
Una limitación (muestra, causalidad o grupo ausente): el grupo de abandono solo tiene 9 clientes e incluye los 4 sin operaciones (gasto 0 €), que bajan su media; la mediana muestra lo contrario (586,81 € frente a 525,01 €). Con 30 clientes la diferencia no es concluyente y no demuestra causalidad.

## 6. Reproducibilidad y defensa individual
Comando ejecutado desde terminal nueva: conda activate mision4 → python pipeline.py (Anaconda PowerShell Prompt, en la carpeta del proyecto). Ruta de CSV / JSON / PNG y resultado de segunda ejecución: salidas/ejecucion_20261028_230333/ con dataset_clientes.csv, informe_validacion.json y gasto_por_abandono.png (válido, 30 filas × 6 columnas). Tras restaurar LEFT JOIN, una nueva ejecución vuelve a ser válida en una carpeta nueva. Comprobación de que una ejecución inválida no genera CSV ni PNG nuevos: con INNER JOIN, la carpeta de esa ejecución solo contiene informe_validacion.json (valido: false, faltan los clientes 7, 14, 21 y 28) y el script termina con "Exportación bloqueada". Cada integrante: función explicada, regla modificada y cambio observado:

Yulianis: explica validar_cliente() (los tres if son independientes para registrar todas las incidencias y return va al final). Modifica una regla: añade la antigüedad máxima de 120 meses (antiguedad_meses > 120 → "Antigüedad superior a 120 meses"). Cambio observado: un cliente de prueba con 130 meses devuelve el nuevo mensaje y los clientes 101–103 mantienen su resultado.
Yuleimis: explica main() en pipeline.py (carpeta nueva por ejecución, informe siempre, CSV y PNG solo si el dataset es válido). Modifica el código: cambia LEFT JOIN por INNER JOIN en consulta_dataset.sql. Cambio observado: 26 filas en lugar de 30, la cobertura detecta que faltan los clientes 7, 14, 21 y 28, valido: false y no se generan CSV ni PNG; al restaurar LEFT JOIN vuelve a ser válido. Ayuda de IA recibida, fragmento revisado y prueba de verificación: asistente de IA (Claude) como guía paso a paso y para proponer el código de validar_cliente, validar_dataset y pipeline.py. Se revisó cada función y se verificó con pruebas: casos del inspector, comparación con Workbench, dataset válido frente a la copia con incidencias y ejecución válida/bloqueada desde una terminal nueva.