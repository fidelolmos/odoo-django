from django.db import models
from .brand import Brand

class VehicleModel(models.Model):
    name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")

    class Meta:
        unique_together = ('name', 'brand')  # Evita nombres repetidos dentro de la misma marca

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class Vehicle(models.Model):
    plate = models.CharField(max_length=20, primary_key=True)
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plate} - {self.model.brand.name} {self.model.name}"