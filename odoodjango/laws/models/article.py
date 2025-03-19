from django.db import models

class Article(models.Model):
    number = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"Artículo {self.number}"