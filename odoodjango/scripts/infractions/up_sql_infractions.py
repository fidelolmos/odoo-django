import os
import subprocess
import time

# Configuración
CONTAINER_NAME = "postgres_db"
SQL_DIR = "/tmp/infractions_infraction"  # Carpeta dentro del contenedor donde están los SQL
DB_NAME = "odoodjango"
DB_USER = "freddy"

def ejecutar_sql_en_contenedor(sql_path, current, total, start_time):
    """Ejecuta un archivo SQL dentro del contenedor de PostgreSQL y muestra progreso"""
    cmd_exec = f'docker exec -i {CONTAINER_NAME} psql -U {DB_USER} -d {DB_NAME} -c "\\i {sql_path};"'
    
    start = time.time()
    result = subprocess.run(cmd_exec, shell=True, capture_output=True, text=True)
    end = time.time()
    
    elapsed = end - start  # Tiempo que tardó en ejecutar el archivo
    avg_time = (end - start_time) / current if current > 1 else elapsed
    remaining_time = avg_time * (total - current)  # Estimación de tiempo restante

    if result.returncode == 0:
        print(f"✅ [{current}/{total}] {sql_path} cargado correctamente. ⏳ ETA: {remaining_time:.2f} segundos")
    else:
        print(f"❌ ERROR al ejecutar {sql_path}. Deteniendo la carga.")
        print(result.stderr)  # Muestra el error específico
        exit(1)

def procesar_carpeta(sql_dir):
    """Obtiene la lista de archivos en el contenedor y los ejecuta en orden"""
    cmd_list = f"docker exec {CONTAINER_NAME} ls -1 {sql_dir} | sort -V"
    try:
        result = subprocess.run(cmd_list, shell=True, capture_output=True, text=True, check=True)
        files = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al listar archivos en {sql_dir}: {e}")
        return

    total_files = len([f for f in files if f.endswith(".sql")])
    print(f"\n🚀 Iniciando la carga de {total_files} archivos SQL en {sql_dir}...\n")

    start_time = time.time()
    for index, file in enumerate(files, start=1):
        if not file.endswith(".sql"):
            continue
        sql_path = os.path.join(sql_dir, file)
        ejecutar_sql_en_contenedor(sql_path, index, total_files, start_time)

# Ejecutar la carga de infractions_infraction
procesar_carpeta(SQL_DIR)

print("\n🎯 Carga de archivos SQL completada.")
