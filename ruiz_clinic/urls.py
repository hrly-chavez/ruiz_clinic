
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
#______________________________DASHBOARD_______________________________ 
      
    path("", views.dashboard, name="dashboard"),

#______________________________APPOINTMENT_______________________________    

    path("appointment/", views.appointment, name="appointment"),
    path("add_appointment/", views.add_appointment, name="add_appointment"),
#______________________________PATIENT_______________________________    

    path("patient/", views.patient, name="patient"),

#______________________________SALES_______________________________    

    path("sales/", views.sales, name='sales'),
    
#______________________________Inventory_______________________________

     path("inventory/", views.inventory, name='inventory'),
     path("add_item/", views.add_item, name='add_item'),

]
