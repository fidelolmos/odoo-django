from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
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
    
class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Neighborhood(models.Model):
    name = models.CharField(max_length=255)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="neighborhoods")

    class Meta:
        unique_together = ('name', 'municipality')  # Evita nombres repetidos dentro de la misma alcaldía

    def __str__(self):
        return f"{self.name}, {self.municipality.name}"

class Location(models.Model):
    street = models.CharField(max_length=255)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name="locations")

    def __str__(self):
        return f"{self.street}, {self.neighborhood.name}, {self.neighborhood.municipality.name}"

class Article(models.Model):
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Artículo {self.number}"


class Fraction(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="fractions")
    number = models.CharField(max_length=10)

    class Meta:
        unique_together = ('article', 'number')

    def __str__(self):
        return f"{self.article} - Fracción {self.number}"


class Subsection(models.Model):
    fraction = models.ForeignKey(Fraction, on_delete=models.CASCADE, related_name="subsections")
    letter = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        unique_together = ('fraction', 'letter')

    def __str__(self):
        return f"{self.fraction} - Inciso {self.letter}" if self.letter else f"{self.fraction}"


class Paragraph(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name="paragraphs")
    number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('subsection', 'number')

    def __str__(self):
        return f"{self.subsection} - Párrafo {self.number}" if self.number else f"{self.subsection}"


class ViolationDetail(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name="violations")
    foundation = models.TextField()  # Fundamentación legal

    def __str__(self):
        return f"{self.paragraph} - {self.foundation[:50]}..."


class Infraction(models.Model):
    infraction_number = models.CharField(max_length=50)  # Número de infracción
    date = models.CharField(max_length=20)  # Fecha
    violation_detail = models.ForeignKey(ViolationDetail, on_delete=models.CASCADE, null =True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False)  # Estado de pago

    def __str__(self):
        return f"{self.infraction_number} - {self.concept}"