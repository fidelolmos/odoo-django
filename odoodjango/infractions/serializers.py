from rest_framework import serializers
from .models import Infraction

class InfractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infraction
        fields = '__all__'  # Incluir todos los campos del modelo
