from django.db import models
from .neighborhood import Neighborhood

class Location(models.Model):
    street = models.CharField(max_length=255)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name="locations")

    def __str__(self):
        return f"{self.street}, {self.neighborhood.name}, {self.neighborhood.municipality.name}"
