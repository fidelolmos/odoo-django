from django.urls import path
from infractions.views import InfractionByPlateView

urlpatterns = [
    path('by-plate/<str:plate>/', InfractionByPlateView.as_view(), name="infraction-by-plate"),
]
