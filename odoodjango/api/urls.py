from django.urls import path
from .views import EmployeeList

urlpatterns = [
    path('employees/', EmployeeList.as_view(), name='employees'),
]
