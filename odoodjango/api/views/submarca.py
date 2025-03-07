import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Configuración de Odoo
ODOO_URL = "http://localhost:8069/jsonrpc"
ODOO_DB = "odoo"
ODOO_USER = "admin"
ODOO_PASSWORD = "admin"

# Función para autenticarse en Odoo
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

# API para CRUD de fleet.submarca
class SubmarcaAPI(APIView):
    
    # Obtener lista de submarcas
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
                    "fleet.submarca", "search_read",
                    [[]],
                    {"fields": ["name", "marca"], "limit": 10}
                ]
            },
            "id": 2
        }

        response = requests.post(ODOO_URL, json=payload).json()
        submarcas = response.get("result", [])

        return Response({"submarcas": submarcas}, status=status.HTTP_200_OK)

    # Crear una nueva submarca
    def post(self, request):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "fleet.submarca", "create",
                    [data]
                ]
            },
            "id": 3
        }

        response = requests.post(ODOO_URL, json=payload).json()
        submarca_id = response.get("result", None)

        if submarca_id:
            return Response({"message": "Submarca creada", "id": submarca_id}, status=status.HTTP_201_CREATED)
        return Response({"error": "Error al crear submarca"}, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar una submarca existente
    def put(self, request, submarca_id):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "fleet.submarca", "write",
                    [[submarca_id], data]
                ]
            },
            "id": 4
        }

        response = requests.post(ODOO_URL, json=payload).json()

        if response.get("result", False):
            return Response({"message": "Submarca actualizada"}, status=status.HTTP_200_OK)
        return Response({"error": "Error al actualizar submarca"}, status=status.HTTP_400_BAD_REQUEST)

    # Eliminar una submarca
    def delete(self, request, submarca_id):
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
                    "fleet.submarca", "unlink",
                    [[submarca_id]]
                ]
            },
            "id": 5
        }

        response = requests.post(ODOO_URL, json=payload).json()

        if response.get("result", False):
            return Response({"message": "Submarca eliminada"}, status=status.HTTP_200_OK)
        return Response({"error": "Error al eliminar submarca"}, status=status.HTTP_400_BAD_REQUEST)
