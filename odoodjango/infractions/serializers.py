from rest_framework import serializers
from infractions.models import Infraction

class InfractionDetailSerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField(source="vehicle.plate")
    brand = serializers.CharField(source="vehicle.model.brand.name")
    model = serializers.CharField(source="vehicle.model.name")
    article = serializers.CharField(source="violation_detail.paragraph.subsection.fraction.article.number")
    fraction = serializers.CharField(source="violation_detail.paragraph.subsection.fraction.number")
    foundation = serializers.CharField(source="violation_detail.foundation")
    colony = serializers.CharField(source="location.neighborhood.name")
    municipality = serializers.CharField(source="location.neighborhood.municipality.name")

    class Meta:
        model = Infraction
        fields = [
            "infraction_number",
            "date",
            "vehicle",
            "brand",
            "model",
            "article",
            "fraction",
            "foundation",
            "colony",
            "municipality",
        ]
