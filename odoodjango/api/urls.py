from django.urls import path
from .views.employes import EmployeeAPI
from .views.fleetmanager_api import VehicleAPI
from .views.submarca import SubmarcaAPI

urlpatterns = [
    path('employees/', EmployeeAPI.as_view(), name='employees_list'),
    path('employees/<int:emp_id>/', EmployeeAPI.as_view(), name='employee_detail'),
    path('vehicles/', VehicleAPI.as_view(), name='vehicles'),
    path('vehicles/<int:vehicle_id>/', VehicleAPI.as_view(), name='vehicle-detail'),
    path('api/submarcas/', SubmarcaAPI.as_view(), name='submarca-list-create'),
    path('api/submarcas/<int:submarca_id>/', SubmarcaAPI.as_view(), name='submarca-detail'),
]