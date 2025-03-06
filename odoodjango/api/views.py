import requests
from rest_framework.response import Response
from rest_framework.views import APIView

# Configuración de Odoo
ODOO_URL = "http://localhost:8069/jsonrpc"
ODOO_DB = "odoo"
ODOO_USER = "admin"
ODOO_PASSWORD = "admin"

# Autenticación en Odoo
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


class EmployeeList(APIView):
    def get(self, request):
        uid = authenticate_odoo()
        if not uid:
            return Response({"error": "No se pudo autenticar en Odoo"}, status=401)

        # Petición a Odoo para obtener empleados
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    ODOO_DB, uid, ODOO_PASSWORD,
                    "emp.empleado", "search_read",
                    [[]],
                    {"fields": ["nombre", "puesto"], "limit": 10}
                ]
            },
            "id": 2
        }

        response = requests.post(ODOO_URL, json=payload).json()
        employees = response.get("result", [])

        return Response({"employees": employees})
