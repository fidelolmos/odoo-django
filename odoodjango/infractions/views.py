from rest_framework.response import Response
from rest_framework import status, generics
from .models import Infraction
from .serializers import InfractionSerializer

class InfractionListView(generics.ListAPIView):
    """
    Endpoint para obtener todas las infracciones (GET)
    """
    queryset = Infraction.objects.all()
    serializer_class = InfractionSerializer

class InfractionCreateView(generics.CreateAPIView):
    """
    Endpoint para crear una nueva infracción (POST)
    """
    queryset = Infraction.objects.all()
    serializer_class = InfractionSerializer

class InfractionDetailView(generics.RetrieveAPIView):
    """
    Endpoint para obtener una infracción por su ID (GET /api/infractions/detail/{id}/)
    """
    queryset = Infraction.objects.all()
    serializer_class = InfractionSerializer
