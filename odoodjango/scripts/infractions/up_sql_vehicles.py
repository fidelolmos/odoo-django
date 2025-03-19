import os
import subprocess

# Configuración
CONTAINER_NAME = "postgres_db"
SQL_DIRS = ["/tmp/locations_location/parts","/tmp/vehicles_vehicle/parts",]  # Carpetas dentro del contenedor
DB_NAME = "odoodjango"
DB_USER = "freddy"

def ejecutar_sql_en_contenedor(sql_path):
    """Ejecuta un archivo SQL dentro del contenedor de PostgreSQL"""
    cmd_exec = f'docker exec -it {CONTAINER_NAME} psql -U {DB_USER} -d {DB_NAME} -c "\\i {sql_path};"'
    try:
        subprocess.run(cmd_exec, shell=True, check=True)
        print(f"✅ {sql_path} cargado correctamente.")
    except subprocess.CalledProcessError:
        print(f"❌ Error al ejecutar {sql_path}. Deteniendo la carga.")
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

    print(f"\n🚀 Iniciando la carga de archivos SQL en {sql_dir}...")

    for file in files:
        if not file.endswith(".sql"):
            continue
        sql_path = os.path.join(sql_dir, file)
        print(f"📂 Cargando {file}...")
        ejecutar_sql_en_contenedor(sql_path)

# Procesar ambas carpetas
for sql_dir in SQL_DIRS:
    procesar_carpeta(sql_dir)

print("\n🎯 Carga de archivos SQL completada.")
