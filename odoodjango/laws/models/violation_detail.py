from django.db import models
from .paragraph import Paragraph

class ViolationDetail(models.Model):
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name="violations")
    foundation = models.TextField()  # Fundamentación legal

    def __str__(self):
        return f"{self.paragraph} - {self.foundation[:50]}..."