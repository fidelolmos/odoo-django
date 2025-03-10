from rest_framework import serializers
from .models import Infraction

class InfractionSerializer(serializers.ModelSerializer):
    # Mapeo de nombres de campos para coincidir con Odoo
    numeroInfraccion = serializers.IntegerField(source="infraction_number")
    fechaInfraccion = serializers.DateField(source="date")
    categoria = serializers.CharField(source="category")
    conceptoInfraccion = serializers.CharField(source="concept")
    vehiculo = serializers.CharField(source="vehicle_plate")
    marca = serializers.CharField(source="brand")
    subMarca = serializers.CharField(source="model")
    calle = serializers.CharField(source="street")
    colonia = serializers.CharField(source="neighborhood")
    alcaldia = serializers.CharField(source="municipality")
    pagado = serializers.BooleanField(source="paid")

    class Meta:
        model = Infraction
        fields = [
            "numeroInfraccion",
            "fechaInfraccion",
            "categoria",
            "conceptoInfraccion",
            "vehiculo",
            "marca",
            "subMarca",
            "calle",
            "colonia",
            "alcaldia",
            "pagado",
        ]
