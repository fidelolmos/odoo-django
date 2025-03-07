import os
import sys
import csv

# Configurar la ruta base del proyecto
BASE_DIR = os.path.join(os.path.dirname(__file__), '../../')
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odoodjango.settings')

# Ruta al archivo CSV
csv_file_path = "/home/freddy-code/Downloads/infractions/infracciones_infracciones_transito_2024_b2.csv"

# Nombre del archivo de salida .sql
output_sql_file = os.path.join(os.path.dirname(__file__), "insert_infractions.sql")

def generate_sql_script():
    with open(csv_file_path, mode='r', encoding='latin-1', errors='replace') as csvfile, open(output_sql_file, mode='w', encoding='utf-8') as sqlfile:
        reader = csv.DictReader(csvfile)

        # Escribimos el encabezado del archivo SQL
        sqlfile.write("BEGIN;\n")  # Iniciar transacción
        
        for row in reader:
            # Eliminar el prefijo "id-" del infraction_number
            infraction_number = row['id_infraccion'].replace("id-", "")

            # Construcción del campo "concept"
            concept = f"{row['articulo']},{row['fraccion']},{row['inciso']},{row['parrafo']}"
            
            # Escapar comillas en los valores para evitar errores de SQL
            values = [
                infraction_number.replace("'", "''"),  # Infraction sin "id-"
                row['fecha_infraccion'].replace("'", "''"),
                row['categoria'].replace("'", "''"),
                concept.replace("'", "''"),
                row['placa'].replace("'", "''"),
                row['marca'].replace("'", "''"),
                row['submarca'].replace("'", "''"),
                row['en_la_calle'].replace("'", "''"),
                row['colonia'].replace("'", "''"),
                row['alcaldia'].replace("'", "''"),
            ]

            # Preparar la consulta SQL con ON CONFLICT DO NOTHING
            sql = (
                "INSERT INTO infractions_infraction "
                "(infraction_number, date, category, concept, vehicle_plate, brand, model, street, neighborhood, municipality, paid) "
                "VALUES "
                f"('{values[0]}', '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}', '{values[5]}', '{values[6]}', '{values[7]}', '{values[8]}', '{values[9]}', FALSE) "
                "ON CONFLICT (infraction_number) DO NOTHING "
                "RETURNING id;\n"
            )


            sqlfile.write(sql)

        sqlfile.write("COMMIT;\n")  # Confirmar transacción

    print(f"✅ Archivo SQL generado correctamente: {output_sql_file}")

if __name__ == '__main__':
    generate_sql_script()
