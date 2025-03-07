from django.db import models

class Infraction(models.Model):
    infraction_number = models.CharField(max_length=50, unique=False)  # Número de infracción
    date = models.CharField(max_length=20)  # Fecha
    category = models.CharField(max_length=100)  # Categoría
    concept = models.CharField(max_length=255)  # Concepto de infracción
    vehicle_plate = models.CharField(max_length=20)  # Placa del vehículo
    brand = models.CharField(max_length=100)  # Marca del vehículo
    model = models.CharField(max_length=100)  # Submarca del vehículo
    street = models.CharField(max_length=255)  # Calle donde ocurrió la infracción
    neighborhood = models.CharField(max_length=255)  # Colonia
    municipality = models.CharField(max_length=255)  # Alcaldía
    paid = models.BooleanField(default=False)  # Estado de pago

    def __str__(self):
        return f"{self.infraction_number} - {self.concept}"
