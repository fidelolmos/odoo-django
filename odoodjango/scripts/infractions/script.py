import os
import sys
import csv

# Configurar la ruta base del proyecto
BASE_DIR = os.path.join(os.path.dirname(__file__), '../../')
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odoodjango.settings')

# Ruta al directorio con los archivos CSV
csv_directory = "/home/freddy-code/Downloads/infractions/"

# Ruta al directorio donde se guardarán los archivos SQL
output_directory = os.path.join(csv_directory, "infractions_sql")

# Crear la carpeta de salida si no existe
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Función para generar el script SQL para cada archivo CSV
def generate_sql_for_all_files():
    # Obtener todos los archivos CSV en el directorio
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

    for csv_file_name in csv_files:
        csv_file_path = os.path.join(csv_directory, csv_file_name)

        # Ruta al archivo de salida .sql en la carpeta infractions_sql
        output_sql_file = os.path.join(output_directory, f"{csv_file_name.replace('.csv', '.sql')}")

        with open(csv_file_path, mode='r', encoding='latin-1', errors='replace') as csvfile, open(output_sql_file, mode='w', encoding='utf-8') as sqlfile:
            reader = csv.DictReader(csvfile)

            # Escribimos el encabezado del archivo SQL
            sqlfile.write("BEGIN;\n")  # Iniciar transacción

            for row in reader:
                # Determinamos el tipo de archivo (si tiene 'id_folio' o 'id_infraccion')
                if 'id_folio' in row:
                    infraction_number = row['id_folio']
                    category = "-----"  # No hay categoría en este tipo de archivo
                else:
                    infraction_number = row['id_infraccion'].replace("id-", "")
                    category = row['categoria'].replace("'", "''")  # Usamos la categoría

                # Construcción del campo "concept"
                concept = f"{row.get('articulo', '')},{row.get('fraccion', '')},{row.get('inciso', '')},{row.get('parrafo', '')}"

                # Usamos .get() para evitar KeyError si alguna columna falta
                values = [
                    infraction_number.replace("'", "''"),
                    row['fecha_infraccion'].replace("'", "''"),
                    category,
                    concept.replace("'", "''"),
                    row['placa'].replace("'", "''"),
                    row['marca'].replace("'", "''"),
                    row.get('submarca', '').replace("'", "''"),  # Usamos .get() aquí para evitar error si no existe
                    row.get('en_la_calle', '').replace("'", "''"),
                    row.get('colonia', '').replace("'", "''"),
                    row.get('alcaldia', '').replace("'", "''"),
                ]

                # Preparar la consulta SQL
                sql = (
                    "INSERT INTO infractions_infraction "
                    "(infraction_number, date, category, concept, vehicle_plate, brand, model, street, neighborhood, municipality, paid) "
                    "VALUES "
                    f"('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}', '{values[5]}', '{values[6]}', '{values[7]}', '{values[8]}', '{values[9]}', FALSE);\n"
                )

                sqlfile.write(sql)

            sqlfile.write("COMMIT;\n")  # Confirmar transacción

        print(f"✅ Archivo SQL generado correctamente: {output_sql_file}")

if __name__ == '__main__':
    generate_sql_for_all_files()
