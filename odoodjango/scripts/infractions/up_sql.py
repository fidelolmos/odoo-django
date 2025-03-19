import os
import subprocess

# Configuración
CONTAINER_NAME = "postgres_db"
SQL_DIRS = ["laws", "vehicles", "locations", "infractions"]  # Orden correcto
BASE_PATH = "/tmp"  # Donde están los archivos dentro del contenedor
DB_NAME = "odoodjango"
DB_USER = "freddy"

def ejecutar_sql_en_contenedor(sql_path, current, total, app_name):
    """Ejecuta un archivo SQL dentro del contenedor y muestra progreso"""
    cmd_exec = f'docker exec -i {CONTAINER_NAME} psql -U {DB_USER} -d {DB_NAME} -f {sql_path}'
    
    result = subprocess.run(cmd_exec, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ [{current}/{total}] {app_name}: {sql_path} cargado correctamente.")
    else:
        print(f"❌ ERROR en {app_name} al ejecutar {sql_path}. Deteniendo.")
        print(result.stderr)  # Muestra el error específico
        exit(1)

def procesar_carpeta(sql_dir):
    """Carga SQLs en el orden correcto"""
    sql_path = os.path.join(BASE_PATH, sql_dir)
    cmd_list = f"docker exec {CONTAINER_NAME} ls -1 {sql_path} | sort -V"

    try:
        result = subprocess.run(cmd_list, shell=True, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al listar archivos en {sql_path}: {e}")
        return

    total_files = len([f for f in files if f.endswith(".sql")])
    print(f"\n🚀 Cargando {total_files} archivos en {sql_dir}...\n")

    for index, file in enumerate(files, start=1):
        if not file.endswith(".sql"):
            continue
        ejecutar_sql_en_contenedor(f"{sql_path}/{file}", index, total_files, sql_dir)

# Procesar todas las aplicaciones en el orden correcto
for app in SQL_DIRS:
    procesar_carpeta(app)

print("\n🎯 Carga de archivos SQL completada en orden correcto.")
