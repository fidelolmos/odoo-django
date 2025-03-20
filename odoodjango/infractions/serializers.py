from rest_framework import serializers
from infractions.models import Infraction

class InfractionDetailSerializer(serializers.ModelSerializer):
    vehicle = serializers.CharField(source="vehicle.plate", default="SIN PLACA")
    brand = serializers.CharField(source="vehicle.model.brand.name", default="DESCONOCIDO")
    model = serializers.CharField(source="vehicle.model.name", default="DESCONOCIDO")
    article = serializers.SerializerMethodField()
    fraction = serializers.SerializerMethodField()
    foundation = serializers.SerializerMethodField()
    colony = serializers.CharField(source="location.neighborhood.name", default="SIN COLONIA")
    municipality = serializers.CharField(source="location.neighborhood.municipality.name", default="SIN MUNICIPIO")
    paid = serializers.BooleanField()

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
            "paid",
        ]

    def get_article(self, obj):
        """ Devuelve el artículo o 'DESCONOCIDO' si violation_detail es NULL """
        if obj.violation_detail and obj.violation_detail.paragraph:
            return getattr(obj.violation_detail.paragraph.subsection.fraction.article, "number", "DESCONOCIDO")
        return "DESCONOCIDO"

    def get_fraction(self, obj):
        """ Devuelve la fracción o 'DESCONOCIDO' si violation_detail es NULL """
        if obj.violation_detail and obj.violation_detail.paragraph:
            return getattr(obj.violation_detail.paragraph.subsection.fraction, "number", "DESCONOCIDO")
        return "DESCONOCIDO"

    def get_foundation(self, obj):
        """ Devuelve la fundamentación o 'SIN FUNDAMENTACIÓN' si violation_detail es NULL """
        return obj.violation_detail.foundation if obj.violation_detail else "SIN FUNDAMENTACIÓN"
