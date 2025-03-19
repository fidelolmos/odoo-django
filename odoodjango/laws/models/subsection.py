from django.db import models
from .fraction import Fraction

class Subsection(models.Model):
    fraction = models.ForeignKey(Fraction, on_delete=models.CASCADE, related_name="subsections")
    letter = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        unique_together = ('fraction', 'letter')

    def __str__(self):
        return f"{self.fraction} - Inciso {self.letter}" if self.letter else f"{self.fraction}"