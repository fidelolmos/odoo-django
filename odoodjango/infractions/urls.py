from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InfractionViewSet

# Crear un router para manejar las rutas automáticamente
router = DefaultRouter()
router.register(r'infractions', InfractionViewSet, basename='infraction')

urlpatterns = [
    path('', include(router.urls)),  # No usar 'api/' aquí
]
