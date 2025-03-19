from django.db import models
from.subsection import Subsection

class Paragraph(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.CASCADE, related_name="paragraphs")
    number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('subsection', 'number')

    def __str__(self):
        return f"{self.subsection} - Párrafo {self.number}" if self.number else f"{self.subsection}"