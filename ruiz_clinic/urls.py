
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
#______________________________DASHBOARD_______________________________ 
      
    path("", views.dashboard, name="dashboard"),

#______________________________APPOINTMENT_______________________________    

    path("appointment/", views.appointment, name="appointment"),
    path("view_appointment/", views.view_appointment, name="view_appointment"),
    path('create/', views.create_appointment, name='create_appointment'),
    path('appointment/edit/', views.edit_appointment, name='edit_appointment'),
    path('delete_appointment/', views.delete_appointment, name='delete_appointment'),
    # path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    # path('get-appointments/', views.get_appointments, name='get-appointments'),
#______________________________PATIENT_______________________________    

    path("patient/", views.patient, name="patient"),

#______________________________SALES_______________________________    

    path("sales/", views.sales, name='sales'),
    
#______________________________Inventory_______________________________

     path("inventory/", views.inventory, name='inventory'),
     path("add_item/", views.add_item, name='add_item'),

]
