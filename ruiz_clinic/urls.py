
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
#______________________________DASHBOARD_______________________________ 
      
    path("", views.dashboard, name="dashboard"),
    path('update-appointment-status/', views.update_appointment_status, name='update_appointment_status'),
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
    path("add_patient/", views.add_patient, name = "add_patient"),
    path("patient/<int:patient_id>/", views.patient_detail, name="patient_detail"),
    path("patient/<int:patient_id>/add_purchase/", views.add_purchased_item, name="add_purchase"),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('item_search/', views.item_search, name='item_search'),
    path('item-price/', views.item_price, name='item_price'),
#______________________________SALES_______________________________    

    path("sales/", views.sales, name='sales'),
    
#______________________________Inventory_______________________________

     path("inventory/", views.inventory, name='inventory'),
     path("add_item/", views.add_item, name='add_item'),
     path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
     path('view_item/<int:item_id>/', views.view_item, name='view_item'),
     path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
]
