from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from infractions.models import Infraction
from infractions.serializers import InfractionDetailSerializer

class InfractionByPlateView(APIView):
    """
    Endpoint para consultar infracciones por número de placa.
    """

    def get(self, request, plate):
        """
        Retorna todas las infracciones asociadas a la placa proporcionada.
        """
        infractions = Infraction.objects.filter(vehicle__plate=plate.upper()).select_related(
            "vehicle__model__brand",
            "violation_detail__paragraph__subsection__fraction__article",
            "location__neighborhood__municipality",
        )

        if infractions.exists():
            serializer = InfractionDetailSerializer(infractions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "No se encontraron infracciones para esta placa."},
                status=status.HTTP_404_NOT_FOUND
            )
