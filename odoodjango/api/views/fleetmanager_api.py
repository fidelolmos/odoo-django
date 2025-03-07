import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# 🔹 Configuración de Odoo
ODOO_URL = "http://localhost:8069/jsonrpc"
ODOO_DB = "odoo"
ODOO_USER = "admin"
ODOO_PASSWORD = "2k23R&Fjdn"

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

# 🔹 API para CRUD de Vehículos
class VehicleAPI(APIView):
    
    # 📌 1️⃣ Obtener lista de vehículos
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
                    "fleet.manager", "search_read",
                    [[]],  # Buscar todos los registros
                    {"fields": ["name", "license_plate", "model_id", "driver_id", "status"]}
                ]
            },
            "id": 2
        }

        response = requests.post(ODOO_URL, json=payload).json()
        vehicles = response.get("result", [])

        return Response({"vehicles": vehicles}, status=status.HTTP_200_OK)

    # 📌 2️⃣ Crear un vehículo nuevo
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
                    "fleet.manager", "create",
                    [data]  # Recibe un diccionario con los datos
                ]
            },
            "id": 3
        }

        response = requests.post(ODOO_URL, json=payload).json()
        vehicle_id = response.get("result", None)

        if vehicle_id:
            return Response({"message": "Vehículo creado", "id": vehicle_id}, status=status.HTTP_201_CREATED)
        return Response({"error": "Error al crear vehículo", "details": response}, status=status.HTTP_400_BAD_REQUEST)

    # 📌 3️⃣ Actualizar un vehículo
    def put(self, request, vehicle_id):
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
                    "fleet.manager", "write",
                    [[vehicle_id], data]  # vehicle_id es el ID del vehículo a actualizar
                ]
            },
            "id": 4
        }

        response = requests.post(ODOO_URL, json=payload).json()

        if response.get("result", False):
            return Response({"message": "Vehículo actualizado"}, status=status.HTTP_200_OK)
        return Response({"error": "Error al actualizar vehículo", "details": response}, status=status.HTTP_400_BAD_REQUEST)

    # 📌 4️⃣ Eliminar un vehículo
    def delete(self, request, vehicle_id):
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
                    "fleet.manager", "unlink",
                    [[vehicle_id]]  # vehicle_id es el ID del vehículo a eliminar
                ]
            },
            "id": 5
        }

        response = requests.post(ODOO_URL, json=payload).json()

        if response.get("result", False):
            return Response({"message": "Vehículo eliminado"}, status=status.HTTP_200_OK)
        return Response({"error": "Error al eliminar vehículo", "details": response}, status=status.HTTP_400_BAD_REQUEST)
