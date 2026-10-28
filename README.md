# Misión 4 · Proyecto del alumno

## Preparación
1. Conserva MySQL Server y Workbench de la Misión 3. Si no tienes su base, ejecuta
   `sql/crear_demo_mysql.sql` UNA VEZ en Workbench. Crea `ai_customer_m4_demo` sin borrar
   `ai_customer`. Si ya existen las tablas demo, consulta al docente antes de cambiarlas.
2. En terminal, entra en esta carpeta (`proyecto`). Con Conda:
   ```sh
   conda create -n mision4 python=3.12
   conda activate mision4
   python -m pip install -r requirements.txt
   python -m ipykernel install --user --name mision4 --display-name "Python (Misión 4)"
   jupyter lab
   ```
   Alternativa sin Conda: `python -m venv .venv`; activa `.venv` (Windows:
   `.venv\Scripts\activate`, macOS/Linux: `source .venv/bin/activate`) y ejecuta los comandos pip/kernel.
3. Copia `.env.example` como `.env`, configura tu usuario local y selecciona DB_NAME.
   Usa `ai_customer` para tu base de la Misión 3 o `ai_customer_m4_demo` para el kit.
   `.env` es un archivo de texto: no cifra ni protege por sí solo las contraseñas.
4. Abre `mision_4.ipynb` y selecciona el kernel Python (Misión 4).

## Archivos
- `validaciones.py` y `pipeline.py`: código de partida con TODO / NotImplementedError.
- `consulta_dataset.sql`: escribe tu consulta; referencia en `sql/consulta_dataset.sql`.
- `datos/dataset_referencia.csv`: 12 clientes sintéticos, incluyendo tres sin operaciones.
- `datos/dataset_con_incidencias.csv`: copia deliberadamente incorrecta para Reto 4.

## Ejecución final
Completa el script y documenta el comando (por ejemplo `python pipeline.py`).
Debe generar una carpeta nueva bajo `salidas/` con informe JSON y, solo cuando pasa
la validación, dataset_clientes.csv y gasto_por_abandono.png.

## Completa antes de entregar
- Mi entorno y versión de Python: …
- Base y origen de los datos: …
- Comando desde terminal y ruta de resultados: …
- Reglas, incidencias y decisiones de tratamiento: …
- Observación del gráfico y limitación: …
- Ayuda de IA recibida y comprobación realizada: …

No entregues `.env`, claves ni capturas que las muestren. Entrega `.env.example` sin
credenciales reales. Reinicia el kernel y ejecuta el notebook de principio a fin.
