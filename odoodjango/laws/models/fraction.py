from django.db import models
from .article import Article

class Fraction(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="fractions")
    number = models.CharField(max_length=10)

    class Meta:
        unique_together = ('article', 'number')

    def __str__(self):
        return f"{self.article} - Fracción {self.number}"