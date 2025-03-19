from django.db import models
from .municipality import Municipality

class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="neighborhoods")

    class Meta:
        unique_together = ('name', 'municipality')  # Evita nombres repetidos dentro de la misma alcaldía

    def __str__(self):
        return f"{self.name}, {self.municipality.name}"