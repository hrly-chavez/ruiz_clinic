
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
]
