import os
import subprocess

# Configuración
CONTAINER_NAME = "postgres_db"
BASE_PATH = "/tmp"  # Carpeta base dentro del contenedor
DB_NAME = "odoodjango"
DB_USER = "freddy"
LOG_FILE = "/tmp/sql_errors.log"  # Archivo de log para errores

# Orden correcto basado en dependencias
SQL_DIRS = [
    "laws_article",
    "laws_fraction",
    "laws_subsection",
    "laws_paragraph",
    "laws_violationdetail",
    "vehicles_brand",
    "vehicles_vehiclemodel",
    "vehicles_vehicle",
    "locations_municipality",
    "locations_neighborhood",
    "locations_location",
    "infractions_infraction"
]

def ejecutar_sql_en_contenedor(sql_path, current, total, app_name):
    """Ejecuta un archivo SQL dentro del contenedor y muestra progreso"""
    cmd_exec = f'docker exec -i {CONTAINER_NAME} psql -U {DB_USER} -d {DB_NAME} --set ON_ERROR_STOP=on -f {sql_path}'
    
    result = subprocess.run(cmd_exec, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ [{current}/{total}] {app_name}: {sql_path} cargado correctamente.")
    else:
        error_message = f"❌ ERROR en {app_name} al ejecutar {sql_path}. Deteniendo.\n{result.stderr}\n"
        print(error_message)
        with open(LOG_FILE, "a") as log:
            log.write(error_message)
        exit(1)

def procesar_carpeta(sql_dir):
    """Carga SQLs en el orden correcto"""
    sql_path = os.path.join(BASE_PATH, sql_dir)

    # Verificar si la carpeta existe dentro del contenedor
    cmd_check = f"docker exec {CONTAINER_NAME} test -d {sql_path}"
    if subprocess.run(cmd_check, shell=True).returncode != 0:
        print(f"⚠️ La carpeta {sql_dir} no existe en {BASE_PATH}. Saltando...")
        return

    # Obtener lista de archivos SQL ordenados
    cmd_list = f"docker exec {CONTAINER_NAME} ls -1 {sql_path} | sort -V"

    try:
        result = subprocess.run(cmd_list, shell=True, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al listar archivos en {sql_path}: {e}")
        return

    sql_files = [f for f in files if f.endswith(".sql")]
    total_files = len(sql_files)

    if total_files == 0:
        print(f"⚠️ No hay archivos SQL en {sql_dir}. Saltando...")
        return

    print(f"\n🚀 Cargando {total_files} archivos en {sql_dir}...\n")

    for index, file in enumerate(sql_files, start=1):
        sql_file_path = os.path.join(sql_path, file)
        ejecutar_sql_en_contenedor(sql_file_path, index, total_files, sql_dir)

# Procesar todas las carpetas en orden correcto
for folder in SQL_DIRS:
    procesar_carpeta(folder)

print("\n🎯 Carga de archivos SQL completada en orden correcto.")
