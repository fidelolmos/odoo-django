import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# 🔹 Configuración de Odoo
ODOO_URL = "http://localhost:8069/jsonrpc"
ODOO_DB = "odoo"
ODOO_USER = "admin"
ODOO_PASSWORD = "admin"

# 🔹 Función para autenticarse en Odoo
def authenticate_odoo():
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": "common",
            "method": "authenticate",
            "args": [ODOO_DB, ODOO_USER, ODOO_PASSWORD, {}]
        },
        "id": 1
    }
    response = requests.post(ODOO_URL, json=payload).json()
    return response.get("result", False)  # Retorna el UID si es exitoso

# 🔹 API para CRUD de empleados
class EmployeeAPI(APIView):
    
    # 📌 1️⃣ Obtener lista de empleados
    def get(self, request):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "emp.empleado", "search_read",
                    [[]],  # Buscar todos los registros
                    {"fields": ["nombre", "puesto"], "limit": 3}
                ]
            },
            "id": 2
        }

        response = requests.post(ODOO_URL, json=payload).json()
        employees = response.get("result", [])

        return Response({"employees": employees}, status=status.HTTP_200_OK)

    # 📌 2️⃣ Crear un empleado nuevo
    def post(self, request):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data  # Obtener datos del frontend

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "emp.empleado", "create",
                    [data]  # Recibe un diccionario con los datos
                ]
            },
            "id": 3
        }

        response = requests.post(ODOO_URL, json=payload).json()
        employee_id = response.get("result", None)

        if employee_id:
            return Response({"message": "Empleado creado", "id": employee_id}, status=status.HTTP_201_CREATED)
        return Response({"error": "Error al crear empleado"}, status=status.HTTP_400_BAD_REQUEST)

    # 📌 3️⃣ Actualizar un empleado
    def put(self, request, emp_id):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data  # Datos del frontend

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "emp.empleado", "write",
                    [[emp_id], data]  # Emp_id es el ID del empleado a actualizar
                ]
            },
            "id": 4
        }

        response = requests.post(ODOO_URL, json=payload).json()

        if response.get("result", False):
            return Response({"message": "Empleado actualizado"}, status=status.HTTP_200_OK)
        return Response({"error": "Error al actualizar empleado"}, status=status.HTTP_400_BAD_REQUEST)

    # 📌 4️⃣ Eliminar un empleado
    def delete(self, request, emp_id):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "emp.empleado", "unlink",
                    [[emp_id]]  # Emp_id es el ID del empleado a eliminar
                ]
            },
            "id": 5
        }

        response = requests.post(ODOO_URL, json=payload).json()

        if response.get("result", False):
            return Response({"message": "Empleado eliminado"}, status=status.HTTP_200_OK)
        return Response({"error": "Error al eliminar empleado"}, status=status.HTTP_400_BAD_REQUEST)
