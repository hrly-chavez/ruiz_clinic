
from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

#_______________________________LOGIN__________________________________
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
#______________________________DASHBOARD_______________________________ 
      
    path("dashboard/", views.dashboard, name="dashboard"),
    path('wordcloud/', views.generate_wordcloud, name='wordcloud'),
    path('update-appointment-status/', views.update_appointment_status, name='update_appointment_status'),
    path('cancel_appointment/', views.cancel_appointment, name='cancel_appointment'),
#______________________________APPOINTMENT_______________________________    

    path("appointment/", views.appointment, name="appointment"),
    path("view_appointment/", views.view_appointment, name="view_appointment"),
    path('create/', views.create_appointment, name='create_appointment'),
    path('appointment/edit/', views.edit_appointment, name='edit_appointment'),
    path('delete_appointment/', views.delete_appointment, name='delete_appointment'),
    path('check_and_update_appointments/', views.check_and_update_appointments, name='check_and_update_appointments'),  # ✅ Add this line
    
#______________________________PATIENT_______________________________    

    path("patient/", views.patient, name="patient"),
    path("add_patient/", views.add_patient, name = "add_patient"),
    path("patient/<int:patient_id>/", views.patient_detail, name="patient_detail"),
    path("patient/<int:patient_id>/add_purchase/", views.add_purchased_item, name="add_purchase"),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('item_search/', views.item_search, name='item_search'),
    path('item-price/', views.item_price, name='item_price'),
    path('edit-purchased-item/<int:purchase_id>/', views.edit_purchased_item, name='edit_purchased_item'),
    path('delete_purchased_item/<int:pur_id>/', views.delete_purchased_item, name='delete_purchased_item'),
    path('edit_patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),

#______________________________SALES_______________________________    

    path("sales/", views.sales_page, name='sales_page'),
    path('api/sales/', views.sales_api, name='sales_api'),
    path("api/patient-balances/", views.patient_balances_api, name="patient_balances_api"),  # New API
    
#______________________________Inventory_______________________________

     path("inventory/", views.inventory, name='inventory'),
     path("add_item/", views.add_item, name='add_item'),
     path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
     path('view_item/<int:item_id>/', views.view_item, name='view_item'),
     path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
     path('inventory/search/', views.search_items, name='search_items'),
#______________________________LOGOUT____________________________________
    path('logout/', views.user_logout, name='logout'),
    
]

