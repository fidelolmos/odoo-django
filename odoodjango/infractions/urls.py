from django.urls import path
from .views import InfractionListView, InfractionCreateView, InfractionDetailView  # Asegúrate de importar InfractionDetailView


urlpatterns = [
    path('infractions/list/', InfractionListView.as_view(), name='infractions-list'),  # GET (Lista todas)
    path('infractions/create/', InfractionCreateView.as_view(), name='infractions-create'),  # POST (Crear nueva)
    path('infractions/detail/<int:pk>/', InfractionDetailView.as_view(), name='infractions-detail'),  # GET (Por ID)
]
