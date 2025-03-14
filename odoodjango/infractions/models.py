from django.db import models
from laws.models import ViolationDetail
from vehicles.models import Vehicle
from locations.models import Location
    
class Infraction(models.Model):
    infraction_number = models.CharField(max_length=50)  # Número de infracción
    date = models.CharField(max_length=20)  # Fecha
    violation_detail = models.ForeignKey(ViolationDetail, on_delete=models.CASCADE, null =True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False)  # Estado de pago

    def __str__(self):
        return f"{self.infraction_number} - {self.date}"