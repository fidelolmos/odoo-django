from rest_framework import viewsets
from .models import Infraction
from .serializers import InfractionSerializer

class InfractionViewSet(viewsets.ModelViewSet):
    queryset = Infraction.objects.all()
    serializer_class = InfractionSerializer
