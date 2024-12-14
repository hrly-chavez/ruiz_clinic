from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointment/", views.appointment, name="appointment"),
    path("inventory/", views.inventory, name='inventory'),
    path("patient/", views.patient, name="patient"),
    path("sales/", views.sales, name='sales'),
]
